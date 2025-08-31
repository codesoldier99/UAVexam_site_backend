"""
改进的手动签到服务模块
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any

from ..models.user import User
from ..models.schedule import Schedule, ScheduleStatus
from ..models.venue import Venue
from ..models.checkin import CheckIn, CheckInStatus, CheckInMethod
from ..models.exam import ExamRegistration, ExamProduct
from ..models.institution import Institution


class ManualCheckinService:
    def __init__(self, db: Session):
        self.db = db

    def query_candidate_for_manual_checkin(self, real_name: str, id_card: str) -> Dict[str, Any]:
        """
        查询考生信息用于手动签到 - 第一步
        
        Args:
            real_name: 考生姓名
            id_card: 身份证号
            
        Returns:
            Dict: 包含考生信息和考试安排的字典
            
        Raises:
            ValueError: 当考生信息不匹配或查询失败时
        """
        try:
            # 1. 验证输入参数
            if not real_name or not real_name.strip():
                raise ValueError("考生姓名不能为空")
            if not id_card or len(id_card.strip()) != 18:
                raise ValueError("请输入18位身份证号")
            
            real_name = real_name.strip()
            id_card = id_card.strip()
            
            # 2. 验证考生身份信息
            candidate = self.db.query(User).filter(
                and_(
                    User.real_name == real_name,
                    User.id_card == id_card,
                    User.role == 'candidate',
                    User.is_active == True
                )
            ).first()
            
            if not candidate:
                raise ValueError("未找到匹配的考生信息，请检查姓名和身份证号是否正确")
            
            # 3. 获取考生所属机构信息
            institution = None
            if candidate.institution_id:
                institution = self.db.query(Institution).filter(
                    Institution.id == candidate.institution_id
                ).first()
            
            # 4. 查询考生当天的考试安排
            today = datetime.now().date()
            
            schedules_query = self.db.query(
                Schedule,
                Venue,
                CheckIn,
                ExamRegistration,
                ExamProduct
            ).join(
                ExamRegistration, Schedule.registration_id == ExamRegistration.id
            ).join(
                ExamProduct, ExamRegistration.exam_product_id == ExamProduct.id
            ).join(
                Venue, Schedule.venue_id == Venue.id
            ).outerjoin(
                CheckIn, and_(
                    Schedule.id == CheckIn.schedule_id,
                    CheckIn.status == CheckInStatus.SUCCESS
                )
            ).filter(
                and_(
                    ExamRegistration.user_id == candidate.id,
                    Schedule.schedule_date == today,
                    ExamRegistration.status == 'approved'  # 只查询已审核通过的报名
                )
            ).order_by(Schedule.start_time).all()
            
            # 5. 构建考试安排详情
            exam_schedules = []
            current_time = datetime.now()
            
            for schedule, venue, checkin, registration, exam_product in schedules_query:
                # 构建考场地址
                venue_address = self._build_venue_address(venue)
                
                # 判断签到状态和是否可以签到
                checkin_status, can_checkin = self._determine_checkin_status(
                    checkin, schedule, current_time
                )
                
                exam_schedule = {
                    "schedule_id": schedule.id,
                    "exam_name": exam_product.name,
                    "exam_type": exam_product.exam_type,
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_address": venue_address,
                    "exam_date": schedule.schedule_date.strftime("%Y-%m-%d"),
                    "start_time": schedule.start_time.strftime("%H:%M:%S"),
                    "end_time": schedule.end_time.strftime("%H:%M:%S"),
                    "status": schedule.status.value,
                    "registration_number": registration.registration_number,
                    "can_checkin": can_checkin,
                    "checkin_status": checkin_status
                }
                exam_schedules.append(exam_schedule)
            
            # 6. 构建响应数据
            candidate_info = {
                "id": candidate.id,
                "real_name": candidate.real_name,
                "id_card": candidate.id_card,
                "phone": candidate.phone,
                "email": candidate.email,
                "institution_name": institution.name if institution else "未分配机构"
            }
            
            # 7. 生成提示信息
            message = self._generate_query_message(exam_schedules)
            
            return {
                "candidate_info": candidate_info,
                "exam_schedules": exam_schedules,
                "message": message
            }
            
        except ValueError:
            raise  # 重新抛出业务逻辑错误
        except Exception as e:
            raise ValueError(f"查询考生信息失败: {str(e)}")
    
    def confirm_manual_checkin(self, candidate_id: int, schedule_id: int, operator_info: str = None) -> Dict[str, Any]:
        """
        确认手动签到 - 第二步
        
        Args:
            candidate_id: 考生ID
            schedule_id: 日程ID
            operator_info: 操作员信息
            
        Returns:
            Dict: 签到结果
        """
        try:
            # 1. 验证考生是否存在
            candidate = self.db.query(User).filter(
                and_(
                    User.id == candidate_id,
                    User.role == 'candidate',
                    User.is_active == True
                )
            ).first()
            
            if not candidate:
                return {
                    "success": False,
                    "message": "考生不存在或已被禁用",
                    "checkin_info": {}
                }
            
            # 2. 验证考试安排是否存在且属于该考生
            schedule_query = self.db.query(
                Schedule,
                Venue,
                ExamRegistration,
                ExamProduct
            ).join(
                ExamRegistration, Schedule.registration_id == ExamRegistration.id
            ).join(
                ExamProduct, ExamRegistration.exam_product_id == ExamProduct.id
            ).join(
                Venue, Schedule.venue_id == Venue.id
            ).filter(
                and_(
                    Schedule.id == schedule_id,
                    ExamRegistration.user_id == candidate_id,
                    ExamRegistration.status == 'approved'
                )
            ).first()
            
            if not schedule_query:
                return {
                    "success": False,
                    "message": "考试安排不存在或不属于该考生",
                    "checkin_info": {}
                }
            
            schedule, venue, registration, exam_product = schedule_query
            
            # 3. 检查是否已经签到
            existing_checkin = self.db.query(CheckIn).filter(
                and_(
                    CheckIn.schedule_id == schedule_id,
                    CheckIn.status == CheckInStatus.SUCCESS
                )
            ).first()
            
            if existing_checkin:
                return {
                    "success": False,
                    "message": "该考生已经签到过，不能重复签到",
                    "checkin_info": {}
                }
            
            # 4. 检查时间窗口（可选，根据业务需求）
            current_time = datetime.now()
            if not self._is_within_checkin_window(schedule, current_time):
                return {
                    "success": False,
                    "message": f"不在签到时间窗口内，签到时间为考试开始前30分钟到考试结束",
                    "checkin_info": {}
                }
            
            # 5. 创建或更新签到记录
            checkin_time = datetime.now(timezone.utc)
            
            # 查找是否有失败的签到记录
            failed_checkin = self.db.query(CheckIn).filter(
                and_(
                    CheckIn.schedule_id == schedule_id,
                    CheckIn.status.in_([CheckInStatus.FAILED, CheckInStatus.INVALID])
                )
            ).first()
            
            if failed_checkin:
                # 更新现有记录
                failed_checkin.status = CheckInStatus.SUCCESS
                failed_checkin.checkin_time = checkin_time
                failed_checkin.method = CheckInMethod.MANUAL
                failed_checkin.notes = f"手动签到 - {operator_info or '工作人员操作'}"
                checkin_record = failed_checkin
            else:
                # 创建新记录
                checkin_record = CheckIn(
                    user_id=candidate_id,
                    schedule_id=schedule_id,
                    venue_id=venue.id,
                    checkin_time=checkin_time,
                    status=CheckInStatus.SUCCESS,
                    method=CheckInMethod.MANUAL,
                    notes=f"手动签到 - {operator_info or '工作人员操作'}"
                )
                self.db.add(checkin_record)
            
            # 6. 提交事务
            self.db.commit()
            
            # 7. 构建响应数据
            checkin_info = {
                "checkin_id": checkin_record.id,
                "checkin_time": checkin_time.isoformat(),
                "method": "MANUAL",
                "operator": operator_info or "工作人员操作",
                "candidate_name": candidate.real_name,
                "exam_name": exam_product.name,
                "venue_name": venue.name
            }
            
            return {
                "success": True,
                "message": "签到成功",
                "checkin_info": checkin_info
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"签到操作失败: {str(e)}",
                "checkin_info": {}
            }
    
    def _build_venue_address(self, venue: Venue) -> str:
        """构建考场地址"""
        address_parts = []
        if hasattr(venue, 'building') and venue.building:
            address_parts.append(venue.building)
        if hasattr(venue, 'floor') and venue.floor:
            address_parts.append(f"{venue.floor}楼")
        if hasattr(venue, 'room_number') and venue.room_number:
            address_parts.append(f"{venue.room_number}室")
        return " ".join(address_parts) if address_parts else venue.name
    
    def _determine_checkin_status(self, checkin: CheckIn, schedule: Schedule, current_time: datetime) -> tuple:
        """判断签到状态和是否可以签到"""
        if checkin and checkin.status == CheckInStatus.SUCCESS:
            return "已签到", False
        elif checkin and checkin.status == CheckInStatus.FAILED:
            return "签到失败", True  # 失败的可以重新签到
        else:
            # 检查时间窗口
            if self._is_within_checkin_window(schedule, current_time):
                return "可签到", True
            else:
                return "不在签到时间", False
    
    def _is_within_checkin_window(self, schedule: Schedule, current_time: datetime) -> bool:
        """检查是否在签到时间窗口内"""
        # 考试开始前30分钟到考试结束
        exam_datetime = datetime.combine(schedule.schedule_date, schedule.start_time)
        exam_end_datetime = datetime.combine(schedule.schedule_date, schedule.end_time)
        
        checkin_start = exam_datetime - timedelta(minutes=30)
        checkin_end = exam_end_datetime
        
        return checkin_start <= current_time <= checkin_end
    
    def _generate_query_message(self, exam_schedules: List[Dict]) -> str:
        """生成查询结果提示信息"""
        if not exam_schedules:
            return "该考生今日无考试安排"
        
        can_checkin_count = sum(1 for schedule in exam_schedules if schedule["can_checkin"])
        
        if can_checkin_count == 0:
            if all(schedule["checkin_status"] == "已签到" for schedule in exam_schedules):
                return "该考生今日所有考试均已签到"
            else:
                return "该考生今日暂无可签到的考试"
        else:
            return f"找到 {len(exam_schedules)} 场考试，其中 {can_checkin_count} 场可以签到"