from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from src.models.schedule import Schedule, ScheduleType, ScheduleStatus, CheckInStatus
from src.models.candidate import Candidate
from src.schemas.schedule import ScheduleCreate, ScheduleUpdate, BatchCreateScheduleRequest, QueuePositionResponse
from src.services.candidate import CandidateService

class ScheduleService:
    @staticmethod
    def create(db: Session, schedule: ScheduleCreate, created_by: int) -> Schedule:
        db_schedule = Schedule(
            candidate_id=schedule.candidate_id,
            exam_date=schedule.exam_date,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            venue_id=schedule.venue_id,
            activity_name=schedule.activity_name,
            status=schedule.status
        )
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        return db_schedule

    @staticmethod
    def get(db: Session, schedule_id: int) -> Optional[Schedule]:
        return db.query(Schedule).filter(Schedule.id == schedule_id).first()

    @staticmethod
    def get_multi(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        candidate_id: Optional[int] = None,
        status: Optional[str] = None,
        scheduled_date: Optional[datetime] = None
    ) -> List[Schedule]:
        query = db.query(Schedule)
        
        if candidate_id:
            query = query.filter(Schedule.candidate_id == candidate_id)
        
        if status:
            query = query.filter(Schedule.status == status)
        
        if scheduled_date:
            query = query.filter(Schedule.scheduled_date == scheduled_date)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session, candidate_id: Optional[int] = None) -> int:
        query = db.query(Schedule)
        if candidate_id:
            query = query.filter(Schedule.candidate_id == candidate_id)
        return query.count()

    @staticmethod
    def update(db: Session, schedule_id: int, schedule: ScheduleUpdate) -> Optional[Schedule]:
        db_schedule = ScheduleService.get(db, schedule_id)
        if db_schedule:
            update_data = schedule.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_schedule, field, value)
            db.commit()
            db.refresh(db_schedule)
        return db_schedule

    @staticmethod
    def delete(db: Session, schedule_id: int) -> bool:
        db_schedule = ScheduleService.get(db, schedule_id)
        if db_schedule:
            db.delete(db_schedule)
            db.commit()
            return True
        return False

    @staticmethod
    def get_candidates_to_schedule(
        db: Session,
        scheduled_date: datetime,
        institution_id: Optional[int] = None,
        exam_product_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Candidate]:
        """获取待排期考生"""
        from src.models.candidate import Candidate
        from src.institutions.models import Institution
        
        query = db.query(Candidate).join(Institution)
        
        if institution_id:
            query = query.filter(Candidate.institution_id == institution_id)
        
        if exam_product_id:
            query = query.filter(Candidate.exam_product_id == exam_product_id)
        
        if status:
            query = query.filter(Candidate.status == status)
        
        # 排除已有排期的考生
        scheduled_candidate_ids = db.query(Schedule.candidate_id).filter(
            Schedule.scheduled_date == scheduled_date
        ).subquery()
        
        query = query.filter(~Candidate.id.in_(scheduled_candidate_ids))
        
        return query.all()

    @staticmethod
    def batch_create_schedules(
        db: Session, 
        request: BatchCreateScheduleRequest, 
        created_by: int
    ) -> List[Schedule]:
        """批量创建排期"""
        schedules = []
        
        for schedule_data in request.schedules:
            try:
                # 创建排期
                schedule = Schedule(
                    candidate_id=schedule_data.candidate_id,
                    exam_product_id=schedule_data.exam_product_id,
                    venue_id=schedule_data.venue_id,
                    scheduled_date=schedule_data.scheduled_date,
                    start_time=schedule_data.start_time,
                    end_time=schedule_data.end_time,
                    schedule_type=schedule_data.schedule_type,
                    status=schedule_data.status,
                    check_in_status="not_checked_in",
                    created_by=created_by
                )
                
                db.add(schedule)
                schedules.append(schedule)
                
            except Exception as e:
                print(f"创建排期失败: {e}")
                continue
        
        db.commit()
        
        # 刷新所有创建的排期以获取ID
        for schedule in schedules:
            db.refresh(schedule)
        
        return schedules

    @staticmethod
    def get_queue_position(db: Session, schedule_id: int) -> Optional[QueuePositionResponse]:
        """获取排队位置"""
        schedule = ScheduleService.get(db, schedule_id)
        if not schedule:
            return None
        
        # 计算排队位置
        queue_query = db.query(Schedule).filter(
            Schedule.scheduled_date == schedule.scheduled_date,
            Schedule.activity_name == schedule.activity_name,
            Schedule.status == "待签到",
            Schedule.id < schedule_id
        )
        
        position = queue_query.count() + 1
        total_in_queue = db.query(Schedule).filter(
            Schedule.scheduled_date == schedule.scheduled_date,
            Schedule.activity_name == schedule.activity_name,
            Schedule.status == "待签到"
        ).count()
        
        return QueuePositionResponse(
            schedule_id=schedule_id,
            position=position,
            total_in_queue=total_in_queue,
            status="waiting"
        )

    @staticmethod
    def check_in(db: Session, schedule_id: int, check_in_time: Optional[datetime] = None) -> Optional[Schedule]:
        """签到"""
        schedule = ScheduleService.get(db, schedule_id)
        if not schedule:
            return None
        
        if check_in_time is None:
            check_in_time = datetime.now()
        
        # 判断是否迟到（超过开始时间15分钟）
        if check_in_time > schedule.start_time + timedelta(minutes=15):
            check_in_status = CheckInStatus.LATE
        else:
            check_in_status = CheckInStatus.CHECKED_IN
        
        schedule.check_in_status = check_in_status
        schedule.check_in_time = check_in_time
        
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def scan_check_in_with_transaction(
        db: Session, 
        schedule_id: int, 
        check_in_time: Optional[datetime] = None,
        notes: Optional[str] = None,
        operator_id: int = None
    ) -> Dict[str, Any]:
        """
        事务安全的扫码签到方法
        
        参数:
        - db: 数据库会话
        - schedule_id: 排期ID
        - check_in_time: 签到时间
        - notes: 备注信息
        - operator_id: 操作员ID
        
        返回:
        - 包含成功状态和详细信息的字典
        """
        try:
            # 获取排期信息（使用行锁）
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).with_for_update().first()
            if not schedule:
                return {
                    "success": False,
                    "error": "排期不存在"
                }
            
            # 检查排期状态
            if schedule.status == "已完成":
                return {
                    "success": False,
                    "error": "该排期已完成，无法签到"
                }
            
            if schedule.status == "已取消":
                return {
                    "success": False,
                    "error": "该排期已取消，无法签到"
                }
            
            # 检查是否已经签到
            if schedule.check_in_status == "已签到":
                return {
                    "success": False,
                    "error": "该考生已经签到"
                }
            
            if schedule.check_in_status == "迟到":
                return {
                    "success": False,
                    "error": "该考生已标记为迟到"
                }
            
            # 设置签到时间
            if check_in_time is None:
                check_in_time = datetime.now()
            
            # 判断是否迟到（超过开始时间15分钟）
            is_late = check_in_time > schedule.start_time + timedelta(minutes=15)
            check_in_status = "迟到" if is_late else "已签到"
            
            # 更新排期表
            schedule.check_in_status = check_in_status
            schedule.check_in_time = check_in_time
            if notes:
                schedule.notes = f"{schedule.notes or ''}\n[签到备注] {notes}"
            
            # 获取考生信息
            candidate = db.query(Candidate).filter(Candidate.id == schedule.candidate_id).first()
            if not candidate:
                return {
                    "success": False,
                    "error": "考生信息不存在"
                }
            
            # 更新考生状态（如果考生状态为待审核，则更新为活跃）
            if candidate.status == "PENDING":
                candidate.status = "ACTIVE"
                candidate.updated_at = datetime.now()
            
            # 获取考试产品信息
            exam_product_name = "未知考试"
            if schedule.exam_product:
                exam_product_name = schedule.exam_product.name
            
            # 提交事务
            db.commit()
            
            return {
                "success": True,
                "candidate_name": candidate.name,
                "exam_product_name": exam_product_name,
                "check_in_status": check_in_status,
                "is_late": is_late,
                "check_in_time": check_in_time,
                "operator_id": operator_id
            }
            
        except Exception as e:
            # 回滚事务
            db.rollback()
            return {
                "success": False,
                "error": f"签到失败: {str(e)}"
            }

    @staticmethod
    def get_check_in_stats(
        db: Session, 
        scheduled_date: Optional[datetime] = None,
        venue_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        获取签到统计信息
        
        参数:
        - db: 数据库会话
        - scheduled_date: 排期日期
        - venue_id: 考场ID
        
        返回:
        - 签到统计信息
        """
        try:
            # 构建查询条件
            query = db.query(Schedule)
            
            if scheduled_date:
                query = query.filter(Schedule.scheduled_date == scheduled_date)
            
            if venue_id:
                query = query.filter(Schedule.venue_id == venue_id)
            
            # 获取总排期数
            total_schedules = query.count()
            
            # 获取已签到数
            checked_in_count = query.filter(Schedule.check_in_status == "已签到").count()
            
            # 获取迟到数
            late_count = query.filter(Schedule.check_in_status == "迟到").count()
            
            # 获取未签到数
            not_checked_in_count = query.filter(Schedule.check_in_status == "未签到").count()
            
            # 计算签到率
            check_in_rate = 0
            if total_schedules > 0:
                check_in_rate = round((checked_in_count + late_count) / total_schedules * 100, 2)
            
            # 获取今日签到统计
            today = datetime.now().date()
            today_query = db.query(Schedule).filter(
                Schedule.scheduled_date >= today,
                Schedule.scheduled_date < today + timedelta(days=1)
            )
            
            if venue_id:
                today_query = today_query.filter(Schedule.venue_id == venue_id)
            
            today_total = today_query.count()
            today_checked_in = today_query.filter(Schedule.check_in_status == "已签到").count()
            today_late = today_query.filter(Schedule.check_in_status == "迟到").count()
            
            return {
                "total_schedules": total_schedules,
                "checked_in_count": checked_in_count,
                "late_count": late_count,
                "not_checked_in_count": not_checked_in_count,
                "check_in_rate": check_in_rate,
                "today_stats": {
                    "total": today_total,
                    "checked_in": today_checked_in,
                    "late": today_late,
                    "not_checked_in": today_total - today_checked_in - today_late
                },
                "date_filter": scheduled_date.isoformat() if scheduled_date else None,
                "venue_filter": venue_id
            }
            
        except Exception as e:
            return {
                "error": f"获取统计信息失败: {str(e)}"
            }

    @staticmethod
    def generate_qr_code(schedule_id: int) -> str:
        """
        生成排期二维码
        
        参数:
        - schedule_id: 排期ID
        
        返回:
        - 二维码内容字符串
        """
        import hashlib
        import time
        
        timestamp = int(time.time())
        content = f"SCHEDULE_{schedule_id}_{timestamp}"
        
        # 生成简单的哈希值作为安全验证
        hash_value = hashlib.md5(content.encode()).hexdigest()[:8]
        
        return f"{content}_{hash_value}"

    @staticmethod
    def validate_qr_code(qr_code: str) -> Optional[int]:
        """
        验证二维码并返回排期ID
        
        参数:
        - qr_code: 二维码内容
        
        返回:
        - 排期ID或None（如果无效）
        """
        try:
            if not qr_code.startswith("SCHEDULE_"):
                return None
            
            parts = qr_code.split("_")
            if len(parts) < 3:
                return None
            
            schedule_id = int(parts[1])
            return schedule_id
            
        except (ValueError, IndexError):
            return None 