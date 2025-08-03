"""
机构数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from src.db.base import Base


class InstitutionStatus(str, enum.Enum):
    """机构状态枚举"""
    active = "active"
    inactive = "inactive"


class Institution(Base):
    """培训机构模型"""
    __tablename__ = "institutions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="机构名称")
    contact_person = Column(String(50), nullable=False, comment="联系人")
    phone = Column(String(20), nullable=False, comment="联系电话")
    status = Column(Enum(InstitutionStatus), default=InstitutionStatus.active, comment="机构状态")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    # candidates = relationship("Candidate", back_populates="institution")
    # users = relationship("User", back_populates="institution")
    
    def __repr__(self):
        return f"<Institution(id={self.id}, name='{self.name}', status='{self.status}')>"