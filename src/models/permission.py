from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.db.base import Base


class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, comment="权限名称")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, primary_key=True, comment="角色ID")
    permission_id = Column(Integer, primary_key=True, comment="权限ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间") 