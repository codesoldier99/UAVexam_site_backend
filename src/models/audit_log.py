"""
审计日志模型
记录所有重要操作的详细信息
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from src.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="操作用户ID")
    username = Column(String(50), nullable=True, comment="操作用户名")
    action = Column(String(50), nullable=False, comment="操作类型")
    resource_type = Column(String(50), nullable=False, comment="资源类型")
    resource_id = Column(Integer, nullable=True, comment="资源ID")
    resource_name = Column(String(255), nullable=True, comment="资源名称")
    method = Column(String(10), nullable=False, comment="HTTP方法")
    endpoint = Column(String(255), nullable=False, comment="API端点")
    ip_address = Column(String(45), nullable=True, comment="客户端IP")
    user_agent = Column(String(500), nullable=True, comment="用户代理")
    request_data = Column(JSON, nullable=True, comment="请求数据")
    response_data = Column(JSON, nullable=True, comment="响应数据")
    old_values = Column(JSON, nullable=True, comment="修改前的值")
    new_values = Column(JSON, nullable=True, comment="修改后的值")
    status_code = Column(Integer, nullable=True, comment="HTTP状态码")
    execution_time = Column(Integer, nullable=True, comment="执行时间(毫秒)")
    error_message = Column(Text, nullable=True, comment="错误信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, user={self.username}, action={self.action}, resource={self.resource_type}:{self.resource_id})>"