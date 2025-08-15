from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class ScheduleStatus(str, enum.Enum):
    PENDING = "pending"          # 待签到
    CHECKED_IN = "checked_in"    # 已签到
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"      # 已完成
    CANCELLED = "cancelled"      # 已取消
    NO_SHOW = "no_show"         # 缺考

class ActivityType(str, enum.Enum):
    THEORY_EXAM = "theory_exam"      # 理论考试
    PRACTICE_EXAM = "practice_exam"  # 实操考试
    WAITING = "waiting"              # 候考

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    exam_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    activity_type = Column(Enum(ActivityType), nullable=False)
    activity_name = Column(String(100))  # e.g., "多旋翼视距内驾驶员理论考试"
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.PENDING)
    check_in_time = Column(DateTime(timezone=True), nullable=True)
    check_in_staff_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    queue_position = Column(Integer, nullable=True)  # 排队位置
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    candidate = relationship("Candidate", back_populates="schedules")
    venue = relationship("Venue", back_populates="schedules")
    check_in_staff = relationship("User", foreign_keys=[check_in_staff_id])