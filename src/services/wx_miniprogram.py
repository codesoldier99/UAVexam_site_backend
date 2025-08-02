from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from src.models.candidate import Candidate
from src.models.schedule import Schedule
from src.models.venue import Venue
from src.schemas.wx_miniprogram import WxLoginResponse, QrCodeResponse

class WxMiniprogramService:
    @staticmethod
    def verify_candidate_by_id_card(db: Session, id_card: str) -> Optional[Candidate]:
        """通过身份证号验证考生"""
        return db.query(Candidate).filter(Candidate.id_number == id_card).first()
    
    @staticmethod
    def get_next_schedule_for_candidate(db: Session, candidate_id: int) -> Optional[Schedule]:
        """获取考生的下一个待办日程"""
        return db.query(Schedule).filter(
            Schedule.candidate_id == candidate_id,
            Schedule.status.in_(['PENDING', 'CONFIRMED']),
            Schedule.scheduled_date >= datetime.now().date()
        ).order_by(Schedule.scheduled_date, Schedule.start_time).first()
    
    @staticmethod
    def get_venue_status(db: Session, venue_id: int) -> dict:
        """获取考场状态"""
        venue = db.query(Venue).filter(Venue.id == venue_id).first()
        if not venue:
            return None
        
        # 获取当前时间段的考试信息
        current_time = datetime.now()
        current_schedules = db.query(Schedule).filter(
            Schedule.venue_id == venue_id,
            Schedule.scheduled_date == current_time.date(),
            Schedule.start_time <= current_time,
            Schedule.end_time >= current_time,
            Schedule.status.in_(['CONFIRMED', 'IN_PROGRESS'])
        ).all()
        
        total_capacity = 10  # 默认容量
        current_occupancy = len(current_schedules)
        status = "空闲" if current_occupancy == 0 else "使用中"
        
        return {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_type": venue.type,
            "status": status,
            "current_occupancy": current_occupancy,
            "total_capacity": total_capacity,
            "occupancy_rate": round(current_occupancy / total_capacity * 100, 1) if total_capacity > 0 else 0
        }
    
    @staticmethod
    def get_all_venues_status(db: Session) -> list:
        """获取所有考场状态"""
        venues = db.query(Venue).filter(Venue.status == 'active').all()
        venues_status = []
        
        for venue in venues:
            status = WxMiniprogramService.get_venue_status(db, venue.id)
            if status:
                venues_status.append(status)
        
        return venues_status 