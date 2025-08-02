from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time, Enum, Text
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
    
    # 关联信息
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, comment="考生ID")
    exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=False, comment="考试产品ID")
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=True, comment="考场ID")
    
    # 时间信息
    scheduled_date = Column(DateTime, nullable=False, comment="排期日期")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    
    # 活动信息
    schedule_type = Column(String(20), nullable=False, comment="排期类型")
    status = Column(String(20), nullable=True, comment="状态")
    check_in_status = Column(String(20), nullable=True, comment="签到状态")
    check_in_time = Column(DateTime, nullable=True, comment="扫码签到时间")
    
    # 排队信息
    queue_position = Column(Integer, nullable=True, comment="排队位置")
    estimated_wait_time = Column(Integer, nullable=True, comment="预计等待时间")
    
    # 备注
    notes = Column(Text, nullable=True, comment="备注")
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID") 