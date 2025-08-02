from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
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
    id_number = Column(String(18), nullable=False, comment="身份证号")
    phone = Column(String(20), nullable=False, comment="联系电话")
    email = Column(String(100), nullable=True, comment="邮箱")
    gender = Column(String(10), nullable=True, comment="性别")
    birth_date = Column(DateTime, nullable=True, comment="出生日期")
    address = Column(Text, nullable=True, comment="地址")
    emergency_contact = Column(String(100), nullable=True, comment="紧急联系人")
    emergency_phone = Column(String(20), nullable=True, comment="紧急联系电话")
    
    # 关联信息
    target_exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=True, comment="目标考试产品ID")
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, comment="所属机构ID")
    exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=False, comment="考试产品ID")
    
    # 状态管理
    status = Column(String(50), default="待审核", comment="考生状态")
    notes = Column(Text, nullable=True, comment="备注")
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID")
    
    # 兼容字段（为了向后兼容）
    id_card = Column(String(18), nullable=False, comment="身份证号") 