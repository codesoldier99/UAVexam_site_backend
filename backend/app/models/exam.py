"""
考试相关数据模型 - 简化版本
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..config.database import Base


class RegistrationStatus(enum.Enum):
    """报名状态枚举"""
    PENDING = "pending"          # 待审核
    CONFIRMED = "confirmed"      # 已确认
    APPROVED = "approved"        # 已批准 (数据库中存在的状态)
    REJECTED = "rejected"        # 已拒绝 (数据库中存在的状态)
    CANCELLED = "cancelled"      # 已取消
    COMPLETED = "completed"      # 已完成



class ExamProduct(Base):
    """考试产品模型"""
    __tablename__ = "exam_products"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    name = Column(String(200), nullable=False, unique=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # 考试配置
    duration_minutes = Column(Integer, nullable=False)  # 考试时长（分钟）
    exam_type = Column(String(50), nullable=False)  # 理论/实操
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 反向关系
    exam_registrations = relationship("ExamRegistration", back_populates="exam_product")
    
    def __repr__(self):
        return f"<ExamProduct {self.name}>"


class ExamRegistration(Base):
    """考试报名模型"""
    __tablename__ = "exam_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联用户
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", back_populates="exam_registrations")
    
    # 关联考试产品
    exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=False, index=True)
    exam_product = relationship("ExamProduct", back_populates="exam_registrations")
    
    # 报名编号
    registration_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # 报名信息
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.PENDING, nullable=False, index=True)
    
    # 备注
    notes = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ExamRegistration {self.id}>"