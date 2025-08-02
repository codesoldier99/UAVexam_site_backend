from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.base import Base
import enum

class CandidateStatus(enum.Enum):
    PENDING_SCHEDULE = "pending_schedule"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    name = Column(String(50), nullable=False, comment="考生姓名")
    id_card = Column(String(18), nullable=False, unique=True, comment="身份证号")
    
    # 关联信息
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, comment="所属机构ID")
    exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=False, comment="考试产品ID")
    
    # 状态管理
    status = Column(String(50), default="待排期", comment="考生状态")
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间") 