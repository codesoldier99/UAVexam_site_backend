"""
审计日志服务
记录和查询系统操作日志
"""

import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from src.models.audit_log import AuditLog
from src.models.user import User
import logging

logger = logging.getLogger(__name__)


class AuditService:
    """审计日志服务"""
    
    @staticmethod
    def log_operation(
        db: Session,
        user: Optional[User],
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        resource_name: Optional[str] = None,
        method: str = "GET",
        endpoint: str = "",
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_data: Optional[Dict] = None,
        response_data: Optional[Dict] = None,
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        status_code: Optional[int] = None,
        execution_time: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """记录操作日志"""
        try:
            audit_log = AuditLog(
                user_id=user.id if user else None,
                username=user.username if user else "Anonymous",
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                resource_name=resource_name,
                method=method,
                endpoint=endpoint,
                ip_address=ip_address,
                user_agent=user_agent,
                request_data=request_data,
                response_data=response_data,
                old_values=old_values,
                new_values=new_values,
                status_code=status_code,
                execution_time=execution_time,
                error_message=error_message
            )
            
            db.add(audit_log)
            db.commit()
            db.refresh(audit_log)
            
            logger.info(f"审计日志记录成功: {action} {resource_type} by {audit_log.username}")
            return audit_log
            
        except Exception as e:
            logger.error(f"记录审计日志失败: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def get_logs(
        db: Session,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        size: int = 50
    ) -> tuple[List[AuditLog], int]:
        """查询审计日志"""
        query = db.query(AuditLog)
        
        # 筛选条件
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if action:
            query = query.filter(AuditLog.action == action)
        
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        
        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)
        
        # 按时间倒序
        query = query.order_by(desc(AuditLog.created_at))
        
        # 获取总数
        total = query.count()
        
        # 分页
        skip = (page - 1) * size
        logs = query.offset(skip).limit(size).all()
        
        return logs, total
    
    @staticmethod
    def get_user_activities(
        db: Session,
        user_id: int,
        days: int = 7
    ) -> List[AuditLog]:
        """获取用户最近活动"""
        start_date = datetime.now() - timedelta(days=days)
        
        logs = db.query(AuditLog).filter(
            and_(
                AuditLog.user_id == user_id,
                AuditLog.created_at >= start_date
            )
        ).order_by(desc(AuditLog.created_at)).limit(100).all()
        
        return logs
    
    @staticmethod
    def get_resource_history(
        db: Session,
        resource_type: str,
        resource_id: int
    ) -> List[AuditLog]:
        """获取资源操作历史"""
        logs = db.query(AuditLog).filter(
            and_(
                AuditLog.resource_type == resource_type,
                AuditLog.resource_id == resource_id
            )
        ).order_by(desc(AuditLog.created_at)).all()
        
        return logs
    
    @staticmethod
    def get_security_events(
        db: Session,
        hours: int = 24
    ) -> List[AuditLog]:
        """获取安全事件（失败的操作）"""
        start_date = datetime.now() - timedelta(hours=hours)
        
        logs = db.query(AuditLog).filter(
            and_(
                AuditLog.created_at >= start_date,
                or_(
                    AuditLog.status_code >= 400,
                    AuditLog.error_message.isnot(None)
                )
            )
        ).order_by(desc(AuditLog.created_at)).all()
        
        return logs
    
    @staticmethod
    def get_statistics(
        db: Session,
        days: int = 30
    ) -> Dict[str, Any]:
        """获取审计统计信息"""
        start_date = datetime.now() - timedelta(days=days)
        
        # 总操作数
        total_operations = db.query(AuditLog).filter(
            AuditLog.created_at >= start_date
        ).count()
        
        # 按操作类型统计
        from sqlalchemy import func
        action_stats = db.query(
            AuditLog.action,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= start_date
        ).group_by(AuditLog.action).all()
        
        # 按资源类型统计
        resource_stats = db.query(
            AuditLog.resource_type,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= start_date
        ).group_by(AuditLog.resource_type).all()
        
        # 活跃用户统计
        active_users = db.query(
            func.count(func.distinct(AuditLog.user_id))
        ).filter(
            and_(
                AuditLog.created_at >= start_date,
                AuditLog.user_id.isnot(None)
            )
        ).scalar()
        
        # 错误操作统计
        error_count = db.query(AuditLog).filter(
            and_(
                AuditLog.created_at >= start_date,
                AuditLog.status_code >= 400
            )
        ).count()
        
        return {
            "period_days": days,
            "total_operations": total_operations,
            "active_users": active_users,
            "error_count": error_count,
            "error_rate": round(error_count / total_operations * 100, 2) if total_operations > 0 else 0,
            "by_action": {action: count for action, count in action_stats},
            "by_resource": {resource: count for resource, count in resource_stats}
        }


class AuditActions:
    """审计操作类型常量"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    BULK_UPDATE = "bulk_update"
    EXPORT = "export"
    IMPORT = "import"


class AuditResources:
    """审计资源类型常量"""
    VENUE = "venue"
    USER = "user"
    ROLE = "role"
    INSTITUTION = "institution"
    EXAM_PRODUCT = "exam_product"
    CANDIDATE = "candidate"
    SCHEDULE = "schedule"