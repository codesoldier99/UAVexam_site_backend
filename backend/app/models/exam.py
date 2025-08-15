from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class VenueType(str, enum.Enum):
    THEORY = "theory"        # 理论考场
    PRACTICE = "practice"    # 实操考场
    WAITING = "waiting"      # 候考场

class ExamProduct(Base):
    __tablename__ = "exam_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    exam_duration_theory = Column(Integer, default=120)  # 理论考试时长(分钟)
    exam_duration_practice = Column(Integer, default=15)  # 实操考试时长(分钟)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    candidates = relationship("Candidate", back_populates="exam_product")

class Venue(Base):
    __tablename__ = "venues"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    type = Column(Enum(VenueType), nullable=False)
    capacity = Column(Integer, default=1)  # 容纳人数
    description = Column(Text)
    location = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    schedules = relationship("Schedule", back_populates="venue")