"""
考试日程安排数据模型 - 简化版本
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Date, Time, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..config.database import Base


class ScheduleStatus(enum.Enum):
    """日程状态枚举"""
    PENDING = "pending"                # 待进行
    IN_PROGRESS = "in_progress"       # 进行中
    COMPLETED = "completed"           # 已完成
    CANCELLED = "cancelled"           # 已取消


class Schedule(Base):
    """考试日程安排模型"""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联报名
    registration_id = Column(Integer, ForeignKey("exam_registrations.id"), nullable=False, index=True)
    registration = relationship("ExamRegistration")
    
    # 关联考场
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False, index=True)
    venue = relationship("Venue")
    
    # 时间安排
    schedule_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # 状态信息
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.PENDING, nullable=False, index=True)
    
    # 考试结果 (新增字段，向后兼容)
    exam_result = Column(String(20))  # pass, fail, absent, pending
    exam_score = Column(Integer)      # 考试分数
    max_score = Column(Integer, default=100)  # 满分
    pass_score = Column(Integer, default=70)  # 及格分
    actual_duration = Column(Integer)  # 实际考试时长(分钟)
    result_notes = Column(Text)       # 考试结果备注
    
    # 备注
    remarks = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系定义
    creator = relationship("User", foreign_keys=[created_by])
    checkins = relationship("CheckIn", back_populates="schedule")
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, date='{self.schedule_date}', time='{self.start_time}-{self.end_time}')>"
