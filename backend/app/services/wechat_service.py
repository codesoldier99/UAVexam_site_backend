from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, case
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json
import hashlib
import secrets
import time
import base64
from io import BytesIO

from ..models.user import User
from ..models.schedule import Schedule, ScheduleStatus
from ..models.venue import Venue
from ..models.checkin import CheckIn, CheckInStatus, CheckInMethod
from ..schemas.wechat import (
    CandidateInfoResponse, 
    CheckinHistoryResponse, 
    ExamResultResponse,
    VenueStatusResponse,
    CandidateScheduleResponse,
    ExamScheduleItem,
    QRCodeGenerationResponse,
    DashboardResponse,
    DashboardStatistics,
    DashboardVenue,
    DashboardAnnouncement,
    WeChatLoginResponse,
    ExamScheduleInfo,
    QRCodeData,
    CheckInResponse
)
from ..utils.qrcode import generate_qr_code

class WeChatService:
    def __init__(self, db: Session):
        self.db = db

    async def get_candidate_by_id_card(self, id_card: str) -> Optional[CandidateInfoResponse]:
        """通过身份证号查询考生信息，包含当前考试安排"""
        try:
            user = self.db.query(User).filter(
                and_(
                    User.id_card == id_card,
                    User.role == 'candidate'
                )
            ).first()
            
            if not user:
                return None
            
            # 获取考生的当前考试安排
            exam_schedules = self.get_candidate_exam_schedules(user.id)
            current_exam = exam_schedules[0] if exam_schedules else None
            
            # 构建基本响应
            response_data = {
                "id": user.id,
                "name": user.real_name or user.username,
                "id_card": user.id_card,
                "phone": user.phone,
                "email": user.email,
                "status": 'active' if user.is_active else 'inactive'
            }
            
            # 如果有当前考试安排，添加考试信息
            if current_exam:
                from datetime import datetime
                exam_datetime = datetime.fromisoformat(current_exam.exam_date.replace('Z', '+00:00'))
                start_time = datetime.strptime(current_exam.start_time, "%H:%M").time()
                end_time = datetime.strptime(current_exam.end_time, "%H:%M").time()
                
                response_data.update({
                    "current_schedule_id": current_exam.schedule_id,
                    "current_venue_id": current_exam.venue_id,
                    "exam_time": datetime.combine(exam_datetime.date(), start_time),
                    "exam_end_time": datetime.combine(exam_datetime.date(), end_time),
                    "venue_name": current_exam.venue_name,
                    "venue_address": current_exam.venue_address,
                    "exam_name": current_exam.exam_name,
                    "exam_type": current_exam.exam_type,
                    "exam_status": current_exam.status
                })
                
            return CandidateInfoResponse(**response_data)
        except Exception as e:
            print(f"Error getting candidate by ID card: {e}")
            return None

    async def refresh_qr_code(self, candidate_id: int) -> Dict[str, Any]:
        """刷新考生二维码，重新获取最新考试安排信息"""
        try:
            # 获取考生信息
            candidate = self.db.query(User).filter(User.id == candidate_id).first()
            if not candidate:
                raise ValueError("考生不存在")

            # 重新获取考生的最新考试安排
            exam_schedules = self.get_candidate_exam_schedules(candidate_id)
            if not exam_schedules:
                raise ValueError("考生没有有效的考试安排")
            
            current_exam = exam_schedules[0]  # 取最近的考试安排

            # 生成新的二维码数据 - 新格式
            current_time = int(time.time())
            qr_data = {
                "candidate_id": candidate_id,
                "name": candidate.real_name or candidate.username,
                "id_card": candidate.id_card,
                "username": candidate.username,
                "schedule_id": current_exam.schedule_id,
                "venue_id": current_exam.venue_id,
                "exam_session": current_exam.exam_session,
                "exam_date": current_exam.exam_date,
                "timestamp": current_time,
                "type": "candidate_checkin"
            }

            # 生成二维码图片
            qr_code_image = generate_qr_code(json.dumps(qr_data))
            
            return {
                "qr_code": qr_code_image,
                "expires_at": datetime.fromtimestamp(current_time + 1800),  # 30分钟后过期
                "refresh_token": secrets.token_urlsafe(32)
            }
        except Exception as e:
            print(f"Error refreshing QR code: {e}")
            raise

    async def get_checkin_history(self, candidate_id: int) -> List[CheckinHistoryResponse]:
        """获取考生签到历史"""
        try:
            checkins = self.db.query(
                CheckIn,
                Schedule,
                Venue
            ).join(
                Schedule, CheckIn.schedule_id == Schedule.id
            ).join(
                Venue, Schedule.venue_id == Venue.id
            ).filter(
                Schedule.candidate_id == candidate_id
            ).order_by(
                CheckIn.checkin_time.desc()
            ).all()

            result = []
            for checkin, schedule, venue in checkins:
                result.append(CheckinHistoryResponse(
                    id=int(checkin.id),
                    schedule_id=int(schedule.id),
                    candidate_id=int(candidate_id),
                    venue_id=int(venue.id),
                    venue_name=str(venue.name),
                    venue_address=str(venue.address) if venue.address else None,
                    checkin_time=checkin.checkin_time,
                    exam_time=schedule.exam_time,
                    exam_end_time=schedule.exam_end_time,
                    exam_type=str(schedule.exam_type) if schedule.exam_type else None,
                    exam_name=str(getattr(schedule, 'exam_name', '考试')),
                    exam_result=str(getattr(schedule, 'exam_result', None)) if getattr(schedule, 'exam_result', None) else None,
                    status=str(checkin.status)
                ))
            
            return result
        except Exception as e:
            print(f"Error getting checkin history: {e}")
            return []

    async def get_exam_results(self, candidate_id: int) -> List[ExamResultResponse]:
        """获取考生考试结果"""
        try:
            results = self.db.query(
                Schedule,
                Venue,
                Checkin
            ).join(
                Venue, Schedule.venue_id == Venue.id
            ).outerjoin(
                CheckIn, Schedule.id == CheckIn.schedule_id
            ).filter(
                and_(
                    Schedule.candidate_id == candidate_id,
                    Schedule.exam_end_time < datetime.now()
                )
            ).order_by(
                Schedule.exam_time.desc()
            ).all()

            result = []
            for schedule, venue, checkin in results:
                result.append(ExamResultResponse(
                    schedule_id=int(schedule.id),
                    candidate_id=int(candidate_id),
                    exam_name=str(getattr(schedule, 'exam_name', '考试')),
                    exam_time=schedule.exam_time,
                    exam_result=str(getattr(schedule, 'exam_result', None)) if getattr(schedule, 'exam_result', None) else None,
                    score=int(getattr(schedule, 'score', None)) if getattr(schedule, 'score', None) else None,
                    status=checkin.status.value if checkin and checkin.status else 'NOT_CHECKED_IN',
                    venue_name=str(venue.name)
                ))
            
            return result
        except Exception as e:
            print(f"Error getting exam results: {e}")
            return []

    async def get_venues_status(self) -> List[VenueStatusResponse]:
        """获取考场状态"""
        try:
            # 获取今日考场使用情况
            today = datetime.now().date()
            
            venues_with_usage = self.db.query(
                Venue,
                func.count(Schedule.id).label('scheduled_count'),
                func.count(
                    case(
                        (and_(
                            CheckIn.status == CheckInStatus.SUCCESS,
                            Schedule.start_time <= datetime.now().time(),
                            Schedule.end_time > datetime.now().time()
                        ), 1)
                    )
                ).label('current_occupied')
            ).outerjoin(
                Schedule, and_(
                    Venue.id == Schedule.venue_id,
                    Schedule.schedule_date == today
                )
            ).outerjoin(
                CheckIn, Schedule.id == CheckIn.schedule_id
            ).group_by(Venue.id).all()

            result = []
            for venue, scheduled_count, current_occupied in venues_with_usage:
                utilization_rate = 0.0
                if venue.capacity and venue.capacity > 0:
                    utilization_rate = round((current_occupied / venue.capacity) * 100, 2)
                
                status = 'AVAILABLE'
                if current_occupied >= venue.capacity:
                    status = 'OCCUPIED'
                elif not venue.is_active:
                    status = 'MAINTENANCE'

                # 构建地址信息
                venue_address_parts = []
                if venue.building:
                    venue_address_parts.append(venue.building)
                if venue.floor:
                    venue_address_parts.append(f"{venue.floor}楼")
                if venue.room_number:
                    venue_address_parts.append(f"{venue.room_number}室")
                venue_address = " ".join(venue_address_parts) if venue_address_parts else venue.name
                
                result.append(VenueStatusResponse(
                    id=venue.id,
                    name=venue.name,
                    address=venue_address,
                    capacity=venue.capacity or 0,
                    current_occupancy=current_occupied or 0,
                    status=status,
                    utilization_rate=utilization_rate
                ))
            
            return result
        except Exception as e:
            print(f"Error getting venues status: {e}")
            return []

    # 新增的三个核心方法

    async def get_candidate_schedule(self, candidate_id: int) -> CandidateScheduleResponse:
        """获取考生考试日程"""
        try:
            # 需要导入ExamRegistration模型
            from ..models.exam import ExamRegistration, ExamProduct
            
            # 查询考生的所有考试安排
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
                ExamRegistration.user_id == candidate_id
            ).order_by(
                Schedule.schedule_date.asc(),
                Schedule.start_time.asc()
            ).all()

            now = datetime.now()
            today = now.date()
            current_time = now.time()
            
            upcoming_exams = []
            completed_exams = []

            for schedule, venue, checkin, registration, exam_product in schedules_query:
                # 构造考场信息
                address_parts = []
                if venue.building:
                    address_parts.append(venue.building)
                if venue.floor:
                    address_parts.append(f"{venue.floor}楼")
                if venue.room_number:
                    address_parts.append(f"{venue.room_number}室")
                
                venue_info = {
                    "id": venue.id,
                    "name": venue.name,
                    "address": " ".join(address_parts) if address_parts else "未指定地址",
                    "capacity": venue.capacity
                }

                # 构造考试时间（合并日期和时间）
                exam_datetime = datetime.combine(schedule.schedule_date, schedule.start_time)
                exam_end_datetime = datetime.combine(schedule.schedule_date, schedule.end_time)

                # 确定考试状态
                status = "scheduled"
                can_checkin = False
                
                if checkin:
                    if checkin.status == CheckInStatus.SUCCESS:
                        if exam_end_datetime <= now:
                            status = "completed"
                        elif exam_datetime <= now:
                            status = "in_progress"
                        else:
                            status = "checked_in"
                    else:
                        status = "scheduled"

                # 检查是否可以签到（考试前30分钟开始）
                if exam_datetime > now:
                    checkin_start_time = exam_datetime - timedelta(minutes=30)
                    can_checkin = now >= checkin_start_time and not checkin
                else:
                    checkin_start_time = None

                exam_item = ExamScheduleItem(
                    schedule_id=schedule.id,
                    exam_name=exam_product.name,
                    exam_time=exam_datetime,
                    exam_end_time=exam_end_datetime,
                    exam_type=exam_product.exam_type,
                    venue=venue_info,
                    status=status,
                    can_checkin=can_checkin,
                    checkin_start_time=checkin_start_time,
                    exam_result=schedule.exam_result,
                    score=schedule.exam_score
                )

                # 按时间分类
                if exam_datetime > now:
                    upcoming_exams.append(exam_item)
                else:
                    completed_exams.append(exam_item)

            # 生成摘要信息
            total_count = len(upcoming_exams) + len(completed_exams)
            next_exam = upcoming_exams[0].exam_time if upcoming_exams else None

            summary = {
                "total_count": total_count,
                "upcoming_count": len(upcoming_exams),
                "completed_count": len(completed_exams),
                "next_exam": next_exam.isoformat() if next_exam else None
            }

            return CandidateScheduleResponse(
                upcoming_exams=upcoming_exams,
                completed_exams=completed_exams,
                summary=summary
            )

        except Exception as e:
            print(f"Error getting candidate schedule: {e}")
            raise

    async def generate_candidate_qrcode(self, candidate_id: int) -> QRCodeGenerationResponse:
        """生成考生二维码，包含当前考试安排信息"""
        try:
            # 获取考生信息
            candidate = self.db.query(User).filter(User.id == candidate_id).first()
            if not candidate:
                raise ValueError("考生不存在")

            # 获取考生的当前考试安排
            exam_schedules = self.get_candidate_exam_schedules(candidate_id)
            if not exam_schedules:
                raise ValueError("考生没有有效的考试安排")
            
            current_exam = exam_schedules[0]  # 取最近的考试安排

            # 构造二维码数据 - 新格式
            current_time = int(time.time())
            qr_data = {
                "candidate_id": candidate_id,
                "name": candidate.real_name or candidate.username,
                "id_card": candidate.id_card,
                "username": candidate.username,
                "schedule_id": current_exam.schedule_id,
                "venue_id": current_exam.venue_id,
                "exam_session": current_exam.exam_session,
                "exam_date": current_exam.exam_date,
                "timestamp": current_time,
                "type": "candidate_checkin"
            }

            # 生成二维码图片
            qr_code_image = generate_qr_code(json.dumps(qr_data))

            # 生成6位数字备用码
            backup_code = f"{secrets.randbelow(900000) + 100000:06d}"

            return QRCodeGenerationResponse(
                qr_code=qr_code_image,
                backup_code=backup_code,
                expires_at=datetime.fromtimestamp(current_time + 1800),  # 30分钟后过期
                refresh_interval=30,
                qr_data=qr_data
            )

        except Exception as e:
            print(f"Error generating candidate QR code: {e}")
            raise

    async def get_dashboard_data(self) -> DashboardResponse:
        """获取公共看板数据"""
        try:
            today = datetime.now().date()
            now = datetime.now()

            # 1. 获取今日考试统计
            stats_query = self.db.query(
                func.count(Schedule.id).label('total_scheduled'),
                func.count(
                    case((CheckIn.status == CheckInStatus.SUCCESS, 1))
                ).label('checked_in'),
                func.count(
                    case((
                        and_(
                            CheckIn.status == CheckInStatus.SUCCESS,
                            Schedule.status == ScheduleStatus.IN_PROGRESS
                        ), 1
                    ))
                ).label('in_progress'),
                func.count(
                    case((
                        and_(
                            CheckIn.status == CheckInStatus.SUCCESS,
                            Schedule.status == ScheduleStatus.COMPLETED
                        ), 1
                    ))
                ).label('completed')
            ).outerjoin(
                CheckIn, Schedule.id == CheckIn.schedule_id
            ).filter(
                Schedule.schedule_date == today
            ).first()

            # 安全地获取统计数据
            total_scheduled = int(stats_query.total_scheduled) if stats_query and stats_query.total_scheduled else 0
            checked_in = int(stats_query.checked_in) if stats_query and stats_query.checked_in else 0
            in_progress = int(stats_query.in_progress) if stats_query and stats_query.in_progress else 0
            completed = int(stats_query.completed) if stats_query and stats_query.completed else 0

            statistics = DashboardStatistics(
                total_scheduled=total_scheduled,
                checked_in=checked_in,
                in_progress=in_progress,
                completed=completed
            )

            # 2. 获取考场状态
            venues_data = await self.get_venues_status()
            venues = [
                DashboardVenue(
                    id=venue.id,
                    name=venue.name,
                    address=venue.address,
                    capacity=venue.capacity,
                    current_occupied=venue.current_occupancy,
                    utilization_rate=venue.utilization_rate,
                    status=venue.status.lower()
                )
                for venue in venues_data
            ]

            # 3. 生成系统公告
            announcements = [
                DashboardAnnouncement(
                    id="ANN_001",
                    title="考试注意事项",
                    content="请考生提前30分钟到达考场，携带有效身份证件",
                    type="notice",
                    priority="high",
                    created_at=datetime.now()
                ),
                DashboardAnnouncement(
                    id="ANN_002",
                    title="系统维护通知",
                    content="系统将于今晚22:00-23:00进行例行维护",
                    type="maintenance",
                    priority="medium",
                    created_at=datetime.now()
                )
            ]

            # 4. 系统状态信息
            system_status = {
                "status": "healthy",
                "uptime": "正常运行",
                "last_updated": datetime.now().isoformat(),
                "version": "1.0.0"
            }

            return DashboardResponse(
                statistics=statistics,
                venues=venues,
                announcements=announcements,
                system_status=system_status
            )

        except Exception as e:
            print(f"Error getting dashboard data: {e}")
            raise

    def query_candidate_for_manual_checkin(self, real_name: str, id_card: str):
        """
        查询考生信息用于手动签到 - 第一步
        
        Args:
            real_name: 考生姓名
            id_card: 身份证号
            
        Returns:
            Dict: 包含考生信息和考试安排的字典
        """
        from ..schemas.wechat import ManualCheckinQueryResponse, ExamScheduleDetail
        from ..models.exam import ExamRegistration, ExamProduct
        from datetime import timezone
        
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
            current_time = datetime.now(timezone.utc)
            
            for schedule, venue, checkin, registration, exam_product in schedules_query:
                # 构建考场地址
                venue_address_parts = []
                if venue.building:
                    venue_address_parts.append(venue.building)
                if venue.floor:
                    venue_address_parts.append(f"{venue.floor}楼")
                if venue.room_number:
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
                    # 检查时间窗口
                    try:
                        self._validate_checkin_time_window(schedule, current_time)
                        can_checkin = True
                        checkin_status = "可签到"
                    except ValueError as e:
                        checkin_status = str(e)
                        can_checkin = False
                
                exam_schedule = ExamScheduleDetail(
                    schedule_id=schedule.id,
                    exam_name=exam_product.name,
                    exam_type=exam_product.exam_type,
                    venue_id=venue.id,
                    venue_name=venue.name,
                    venue_address=venue_address,
                    exam_date=schedule.schedule_date.strftime("%Y-%m-%d"),
                    start_time=schedule.start_time.strftime("%H:%M:%S"),
                    end_time=schedule.end_time.strftime("%H:%M:%S"),
                    status=schedule.status.value,
                    registration_number=registration.registration_number,
                    can_checkin=can_checkin,
                    checkin_status=checkin_status
                )
                exam_schedules.append(exam_schedule)
            
            # 4. 构建响应数据
            candidate_info = {
                "id": candidate.id,
                "real_name": candidate.real_name,
                "id_card": candidate.id_card,
                "phone": candidate.phone
            }
            
            # 检查是否有可签到的考试
            can_checkin_count = sum(1 for schedule in exam_schedules if schedule.can_checkin)
            message = None
            if can_checkin_count == 0:
                if all(schedule.checkin_status == "已签到" for schedule in exam_schedules):
                    message = "该考生今日所有考试均已签到"
                else:
                    message = "该考生今日暂无可签到的考试"
            
            return {
                "candidate_info": candidate_info,
                "exam_schedules": [schedule.dict() for schedule in exam_schedules],
                "message": message
            }
            
        except Exception as e:
            raise ValueError(f"查询考生信息失败: {str(e)}")
    
    def confirm_manual_checkin(self, candidate_id: int, schedule_id: int, operator_info: str = None):
        """
        确认手动签到 - 第二步
        
        Args:
            candidate_id: 考生ID
            schedule_id: 日程ID
            operator_info: 操作员信息
            
        Returns:
            Dict: 签到结果
        """
        from ..schemas.wechat import ManualCheckinConfirmResponse
        from ..models.exam import ExamRegistration, ExamProduct
        from datetime import timezone
        
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
            
            # 3. 验证时间窗口
            current_time = datetime.now(timezone.utc)
            self._validate_checkin_time_window(schedule, current_time)
            
            # 4. 检查是否已经签到
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
            raise ValueError(str(e))
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"签到操作失败: {str(e)}")
            raise ValueError(f"签到操作失败: {str(e)}")
    
    def _validate_checkin_time_window(self, schedule, current_time):
        """验证签到时间窗口 - 手动签到无时间限制"""
        # 手动签到不设置时间限制，跟二维码签到一样
        # 只检查考试日期是否为今天
        current_date = datetime.now().date()
        exam_date = schedule.schedule_date
        
        # 只验证是否为考试当天，不限制具体时间
        if exam_date != current_date:
            if exam_date > current_date:
                days_until = (exam_date - current_date).days
                raise ValueError(f"考试将在 {exam_date.strftime('%Y年%m月%d日')} 举行（还有{days_until}天）")
            else:
                days_passed = (current_date - exam_date).days
                raise ValueError(f"考试已结束，考试日期为 {exam_date.strftime('%Y年%m月%d日')}（已过去{days_passed}天）")
        
        # 考试当天，手动签到无时间限制
        pass

    def process_checkin(self, examiner_id: int, qr_code_data: str):
        """
        处理考务人员签到操作 - 新版本，从二维码中获取所有信息
        
        Args:
            examiner_id: 考务人员ID
            qr_code_data: 包含完整信息的二维码JSON字符串
        
        Returns:
            CheckInResponse: 签到结果
        """
        from ..schemas.wechat import CheckInResponse
        from ..models.user import UserRole
        import json
        
        try:
            # 1. 解析二维码数据获取所有信息
            try:
                qr_data = json.loads(qr_code_data)
                
                # 验证二维码数据的完整性
                required_fields = ["candidate_id", "name", "id_card", "username", "schedule_id", "venue_id", "timestamp", "type"]
                for field in required_fields:
                    if field not in qr_data:
                        raise ValueError(f"二维码数据缺少必要字段: {field}")
                
                if qr_data["type"] != "candidate_checkin":
                    raise ValueError("无效的二维码类型")
                
                # 验证时间戳（防止过期二维码）
                import time
                current_time = int(time.time())
                if current_time - qr_data["timestamp"] > 1800:  # 30分钟过期
                    raise ValueError("二维码已过期，请刷新后重试")
                
                # 提取关键信息
                candidate_id = qr_data["candidate_id"]
                schedule_id = qr_data["schedule_id"]
                venue_id = qr_data["venue_id"]
                
            except json.JSONDecodeError:
                raise ValueError("二维码数据格式错误")
            except Exception as e:
                raise ValueError(f"二维码验证失败: {str(e)}")
            
            # 2. 验证考试安排是否存在
            schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                raise ValueError(f"考试安排不存在: {schedule_id}")
            
            # 3. 验证考场是否存在且匹配
            venue = self.db.query(Venue).filter(Venue.id == venue_id).first()
            if not venue:
                raise ValueError(f"考场不存在: {venue_id}")
            
            if schedule.venue_id != venue_id:
                raise ValueError(f"考试安排的考场({schedule.venue_id})与二维码中的考场({venue_id})不匹配")
            
            # 4. 验证考务人员权限
            examiner = self.db.query(User).filter(User.id == examiner_id).first()
            if not examiner:
                raise ValueError(f"考务人员不存在: {examiner_id}")
            
            if examiner.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EXAMINER]:
                raise ValueError("只有考务人员可以执行签到操作")
            
            # 5. 验证考生信息
            candidate = self.db.query(User).filter(User.id == candidate_id).first()
            if not candidate:
                raise ValueError(f"考生不存在: {candidate_id}")
            
            # 验证二维码中的考生信息与数据库匹配
            if qr_data["id_card"] != candidate.id_card:
                raise ValueError("二维码中的身份证信息与考生不匹配")
            
            if qr_data["username"] != candidate.username:
                raise ValueError("二维码中的用户名与考生不匹配")
            
            # 6. 检查是否已经签到过
            existing_checkin = self.db.query(CheckIn).filter(
                CheckIn.schedule_id == schedule_id
            ).first()
            
            if existing_checkin:
                # 构建地址信息
                venue_address_parts = []
                if venue.building:
                    venue_address_parts.append(venue.building)
                if venue.floor:
                    venue_address_parts.append(f"{venue.floor}楼")
                if venue.room_number:
                    venue_address_parts.append(f"{venue.room_number}室")
                venue_address = " ".join(venue_address_parts) if venue_address_parts else venue.name
                
                return CheckInResponse(
                    success=False,
                    message="该考试安排已完成签到",
                    checkin_time=existing_checkin.checkin_time,
                    schedule_info={
                        "schedule_id": schedule_id,
                        "venue_name": venue.name,
                        "venue_address": venue_address,
                        "status": "already_checked_in",
                        "candidate_name": candidate.real_name or candidate.username
                    }
                )
            
            # 7. 验证考试时间窗口（允许提前30分钟签到，考试结束后30分钟内仍可签到）
            from datetime import datetime, timedelta, date
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            
            if schedule.schedule_date and schedule.start_time:
                exam_date = schedule.schedule_date
                exam_datetime = datetime.combine(exam_date, schedule.start_time)
                exam_end_datetime = datetime.combine(exam_date, schedule.end_time) if schedule.end_time else exam_datetime + timedelta(hours=2)
                
                # 首先检查考试日期
                if current_date < exam_date:
                    # 考试还未到日期
                    days_until_exam = (exam_date - current_date).days
                    raise ValueError(f"考试日期未到，考试将在 {exam_date.strftime('%Y年%m月%d日')} 举行（还有{days_until_exam}天）")
                elif current_date > exam_date:
                    # 考试日期已过
                    days_since_exam = (current_date - exam_date).days
                    raise ValueError(f"考试已结束，考试日期为 {exam_date.strftime('%Y年%m月%d日')}（已过去{days_since_exam}天）")
                else:
                    # 考试当天，检查时间窗口
                    checkin_start_time = exam_datetime - timedelta(minutes=30)
                    checkin_end_time = exam_end_datetime + timedelta(minutes=30)
                    
                    if current_datetime < checkin_start_time:
                        raise ValueError(f"签到时间未到，请在 {checkin_start_time.strftime('%H:%M')} 后签到")
                    elif current_datetime > checkin_end_time:
                        raise ValueError(f"签到时间已过，签到截止时间为 {checkin_end_time.strftime('%H:%M')}")
            
            # 8. 创建签到记录
            checkin_record = CheckIn(
                user_id=candidate_id,
                venue_id=venue_id,
                schedule_id=schedule_id,
                staff_id=examiner_id,
                checkin_time=current_datetime,
                method=CheckInMethod.QR_CODE,
                status=CheckInStatus.SUCCESS,
                notes=f"考务人员{examiner.real_name or examiner.username}为考生{candidate.real_name or candidate.username}执行签到",
                data=json.dumps({
                    "qr_code_data": qr_data,
                    "candidate_info": {
                        "id": candidate_id,
                        "name": candidate.real_name or candidate.username,
                        "id_card": candidate.id_card,
                        "username": candidate.username
                    },
                    "examiner_info": {
                        "id": examiner_id,
                        "name": examiner.real_name or examiner.username,
                        "role": examiner.role.value
                    }
                })
            )
            
            # 9. 更新考试安排状态
            if schedule.status == ScheduleStatus.PENDING:
                schedule.status = ScheduleStatus.IN_PROGRESS
            
            # 10. 保存到数据库
            self.db.add(checkin_record)
            self.db.commit()
            self.db.refresh(checkin_record)
            
            # 11. 构造返回结果
            venue_address_parts = []
            if venue.building:
                venue_address_parts.append(venue.building)
            if venue.floor:
                venue_address_parts.append(f"{venue.floor}楼")
            if venue.room_number:
                venue_address_parts.append(f"{venue.room_number}室")
            venue_address = " ".join(venue_address_parts) if venue_address_parts else venue.name
            
            schedule_info = {
                "schedule_id": schedule_id,
                "venue_name": venue.name,
                "venue_address": venue_address,
                "exam_time": f"{schedule.schedule_date} {schedule.start_time}" if schedule.schedule_date and schedule.start_time else None,
                "status": schedule.status.value,
                "candidate_name": candidate.real_name or candidate.username,
                "candidate_id": candidate_id,
                "examiner": {
                    "id": examiner_id,
                    "name": examiner.real_name or examiner.username
                }
            }
            
            return CheckInResponse(
                success=True,
                message="签到成功",
                checkin_time=checkin_record.checkin_time,
                schedule_info=schedule_info
            )
            
        except ValueError as e:
            # 业务逻辑错误
            print(f"签到业务逻辑错误: {str(e)}")
            raise e
        except Exception as e:
            # 数据库或其他系统错误
            print(f"签到系统错误: {str(e)}")
            import traceback
            traceback.print_exc()
            self.db.rollback()
            raise ValueError(f"签到处理失败: {str(e)}")

    def login_by_id_card(self, id_card: str, openid: str = None):
        """
        通过身份证号登录，返回完整的考试安排信息
        
        Args:
            id_card: 身份证号
            openid: 微信openid（可选）
            
        Returns:
            WeChatLoginResponse: 包含用户信息和考试安排的完整响应
        """
        try:
            # 1. 查找用户
            user = self.db.query(User).filter(
                and_(
                    User.id_card == id_card,
                    User.is_active == True
                )
            ).first()
            
            if not user:
                raise ValueError("用户不存在或已被禁用")
            
            # 2. 更新微信openid（如果提供）
            if openid and user.wechat_openid != openid:
                user.wechat_openid = openid
                user.last_login = datetime.now()
                self.db.commit()
            
            # 3. 生成访问令牌
            from ..utils.security import create_access_token
            from datetime import timedelta
            from ..config.settings import settings
            
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = create_access_token(
                data={"sub": user.username, "user_id": user.id, "role": user.role.value},
                expires_delta=access_token_expires
            )
            
            # 4. 获取考试安排信息
            exam_schedules = self.get_candidate_exam_schedules(user.id)
            
            # 5. 构建响应
            user_info = {
                "id": user.id,
                "username": user.username,
                "name": user.real_name or user.username,
                "id_card": user.id_card,
                "phone": user.phone,
                "email": user.email,
                "role": user.role.value
            }
            
            # 找到当前最近的考试安排
            current_exam = None
            upcoming_exams = []
            
            if exam_schedules:
                # 按时间排序，最近的考试作为current_exam
                current_exam = exam_schedules[0] if exam_schedules else None
                upcoming_exams = exam_schedules[1:] if len(exam_schedules) > 1 else []
            
            from ..schemas.wechat import WeChatLoginResponse
            return WeChatLoginResponse(
                access_token=access_token,
                token_type="bearer",
                user_info=user_info,
                current_exam=current_exam,
                upcoming_exams=upcoming_exams,
                has_valid_schedule=len(exam_schedules) > 0
            )
            
        except Exception as e:
            print(f"登录错误: {str(e)}")
            import traceback
            traceback.print_exc()
            raise ValueError(f"登录失败: {str(e)}")

    def get_candidate_exam_schedules(self, candidate_id: int):
        """
        获取考生的有效考试安排
        
        Args:
            candidate_id: 考生ID
            
        Returns:
            List[ExamScheduleInfo]: 考试安排列表
        """
        try:
            # 导入必要的模型
            from ..models.exam import ExamRegistration, ExamProduct
            from datetime import date
            
            # 查询考生的有效考试安排
            schedules_query = self.db.query(
                Schedule,
                Venue,
                ExamProduct,
                ExamRegistration,
                User
            ).join(
                ExamRegistration, Schedule.registration_id == ExamRegistration.id
            ).join(
                ExamProduct, ExamRegistration.exam_product_id == ExamProduct.id
            ).join(
                Venue, Schedule.venue_id == Venue.id
            ).join(
                User, ExamRegistration.user_id == User.id
            ).filter(
                and_(
                    ExamRegistration.user_id == candidate_id,
                    Schedule.status.in_([ScheduleStatus.PENDING, ScheduleStatus.IN_PROGRESS]),
                    Schedule.schedule_date >= date.today()
                )
            ).order_by(
                Schedule.schedule_date,
                Schedule.start_time
            ).all()
            
            exam_schedules = []
            for schedule, venue, exam_product, registration, user in schedules_query:
                # 构建地址信息
                venue_address_parts = []
                if venue.building:
                    venue_address_parts.append(venue.building)
                if venue.floor:
                    venue_address_parts.append(f"{venue.floor}楼")
                if venue.room_number:
                    venue_address_parts.append(f"{venue.room_number}室")
                venue_address = " ".join(venue_address_parts) if venue_address_parts else venue.name
                
                # 确定考试时段
                start_hour = schedule.start_time.hour if schedule.start_time else 9
                if start_hour < 12:
                    exam_session = "morning"
                elif start_hour < 18:
                    exam_session = "afternoon"
                else:
                    exam_session = "evening"
                
                from ..schemas.wechat import ExamScheduleInfo
                exam_info = ExamScheduleInfo(
                    schedule_id=schedule.id,
                    venue_id=venue.id,
                    exam_date=schedule.schedule_date.isoformat(),
                    exam_session=exam_session,
                    start_time=schedule.start_time.strftime("%H:%M") if schedule.start_time else "09:00",
                    end_time=schedule.end_time.strftime("%H:%M") if schedule.end_time else "11:00",
                    venue_name=venue.name,
                    venue_address=venue_address,
                    exam_name=exam_product.name,
                    exam_type=exam_product.exam_type,
                    registration_number=registration.registration_number,
                    status=schedule.status.value
                )
                exam_schedules.append(exam_info)
            
            return exam_schedules
            
        except Exception as e:
            print(f"获取考试安排错误: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
