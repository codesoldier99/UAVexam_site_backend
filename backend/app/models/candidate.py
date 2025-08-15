from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class CandidateStatus(str, enum.Enum):
    PENDING_SCHEDULE = "pending_schedule"      # 待排期
    SCHEDULED = "scheduled"                    # 已排期
    THEORY_WAITING = "theory_waiting"          # 待理论考试
    THEORY_COMPLETED = "theory_completed"      # 理论考试完成
    PRACTICE_WAITING = "practice_waiting"      # 待实操考试
    PRACTICE_IN_PROGRESS = "practice_in_progress"  # 实操考试中
    COMPLETED = "completed"                    # 考试完成
    CANCELLED = "cancelled"                    # 已取消

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    id_card = Column(String(18), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    email = Column(String(100))
    wechat_openid = Column(String(128), unique=True, index=True, nullable=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=False)
    status = Column(Enum(CandidateStatus), default=CandidateStatus.PENDING_SCHEDULE)
    queue_number = Column(Integer, nullable=True)  # 排队号码
    current_venue_id = Column(Integer, ForeignKey("venues.id"), nullable=True)  # 当前所在考场
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    institution = relationship("Institution", back_populates="candidates")
    exam_product = relationship("ExamProduct", back_populates="candidates")
    schedules = relationship("Schedule", back_populates="candidate")
    current_venue = relationship("Venue", foreign_keys=[current_venue_id])