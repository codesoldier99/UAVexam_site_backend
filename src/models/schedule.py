from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.base import Base
import enum

class ScheduleType(enum.Enum):
    THEORY = "theory"
    PRACTICAL = "practical"
    WAITING = "waiting"

class ScheduleStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class CheckInStatus(enum.Enum):
    NOT_CHECKED_IN = "not_checked_in"
    CHECKED_IN = "checked_in"
    LATE = "late"

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    
    # 时间信息
    exam_date = Column(Date, nullable=False, comment="考试日期")
    start_time = Column(Time, nullable=False, comment="开始时间")
    end_time = Column(Time, nullable=False, comment="结束时间")
    
    # 关联信息
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, comment="考生ID")
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False, comment="考场ID")
    
    # 活动信息
    activity_name = Column(String(100), nullable=False, comment="活动名称")
    status = Column(String(50), default="待签到", comment="日程状态")
    check_in_time = Column(DateTime, nullable=True, comment="扫码签到时间")
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间") 