"""
手动签到服务模块
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
        """
        try:
            # 1. 验证考生身份信息
            candidate = self.db.query(User).filter(
                and_(
                    User.real_name == real_name,
                    User.id_card == id_card,
                    User.role == 'candidate'
                )
            ).first()
            
            if not candidate:
                raise ValueError("考生信息不匹配，请检查姓名和身份证号")
            
            # 2. 查询考生当天的考试安排
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
                CheckIn, Schedule.id == CheckIn.schedule_id
            ).filter(
                and_(
                    ExamRegistration.user_id == candidate.id,
                    Schedule.schedule_date == today
                )
            ).order_by(Schedule.start_time).all()
            
            if not schedules_query:
                return {
                    "candidate_info": {
                        "id": candidate.id,
                        "real_name": candidate.real_name,
                        "id_card": candidate.id_card,
                        "phone": candidate.phone
                    },
                    "exam_schedules": [],
                    "message": "该考生今日无考试安排"
                }
            
            # 3. 构建考试安排详情
            exam_schedules = []
            current_time = datetime.now()
            
            for schedule, venue, checkin, registration, exam_product in schedules_query:
                # 构建考场地址
                venue_address_parts = []
                if hasattr(venue, 'building') and venue.building:
                    venue_address_parts.append(venue.building)
                if hasattr(venue, 'floor') and venue.floor:
                    venue_address_parts.append(f"{venue.floor}楼")
                if hasattr(venue, 'room_number') and venue.room_number:
                    venue_address_parts.append(f"{venue.room_number}室")
                venue_address = " ".join(venue_address_parts) if venue_address_parts else venue.name
                
                # 判断签到状态和是否可以签到
                checkin_status = "未签到"
                can_checkin = False
                
                if checkin and checkin.status == CheckInStatus.SUCCESS:
                    checkin_status = "已签到"
                elif checkin and checkin.status == CheckInStatus.FAILED:
                    checkin_status = "签到失败"
                    can_checkin = True  # 失败的可以重新签到
                else:
                    # 移除时间窗口限制，与二维码签到保持一致
                    can_checkin = True
                    checkin_status = "可签到"
                
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
            
            # 4. 构建响应数据
            candidate_info = {
                "id": candidate.id,
                "real_name": candidate.real_name,
                "id_card": candidate.id_card,
                "phone": candidate.phone
            }
            
            # 检查是否有可签到的考试
            can_checkin_count = sum(1 for schedule in exam_schedules if schedule["can_checkin"])
            message = None
            if can_checkin_count == 0:
                if all(schedule["checkin_status"] == "已签到" for schedule in exam_schedules):
                    message = "该考生今日所有考试均已签到"
                else:
                    message = "该考生今日暂无可签到的考试"
            
            return {
                "candidate_info": candidate_info,
                "exam_schedules": exam_schedules,
                "message": message
            }
            
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
                    User.role == 'candidate'
                )
            ).first()
            
            if not candidate:
                raise ValueError("考生不存在")
            
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
                    ExamRegistration.user_id == candidate_id
                )
            ).first()
            
            if not schedule_query:
                raise ValueError("考试安排不存在或不属于该考生")
            
            schedule, venue, registration, exam_product = schedule_query
            
            # 3. 检查是否已经签到
            existing_checkin = self.db.query(CheckIn).filter(
                and_(
                    CheckIn.schedule_id == schedule_id,
                    CheckIn.status == CheckInStatus.SUCCESS
                )
            ).first()
            
            if existing_checkin:
                raise ValueError("该考生已经签到，无需重复签到")
            
            # 5. 创建签到记录
            checkin_time = datetime.now(timezone.utc)
            
            # 如果之前有失败的签到记录，更新它；否则创建新记录
            checkin_record = self.db.query(CheckIn).filter(
                CheckIn.schedule_id == schedule_id
            ).first()
            
            if checkin_record:
                # 更新现有记录
                checkin_record.status = CheckInStatus.SUCCESS
                checkin_record.checkin_time = checkin_time
                checkin_record.method = CheckInMethod.MANUAL
                checkin_record.notes = f"手动签到 - {operator_info or '工作人员操作'}"
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
                "checkin_time": checkin_time.isoformat(),
                "candidate_name": candidate.real_name,
                "exam_name": exam_product.name,
                "venue_name": venue.name,
                "checkin_method": "手动签到",
                "operator_info": operator_info or "工作人员操作"
            }
            
            return {
                "success": True,
                "message": "签到成功",
                "checkin_info": checkin_info
            }
            
        except ValueError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": str(e),
                "checkin_info": {}
            }
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"签到操作失败: {str(e)}")
    

