"""
审计装饰器
自动记录API操作日志
"""

import time
import json
from functools import wraps
from typing import Callable, Optional, Dict, Any
from fastapi import Request
from sqlalchemy.orm import Session
from src.services.audit_service import AuditService, AuditActions, AuditResources
from src.models.user import User
import logging

logger = logging.getLogger(__name__)


def audit_operation(
    action: str,
    resource_type: str,
    get_resource_id: Optional[Callable] = None,
    get_resource_name: Optional[Callable] = None,
    capture_request: bool = True,
    capture_response: bool = False,
    capture_changes: bool = False
):
    """
    审计装饰器
    
    Args:
        action: 操作类型
        resource_type: 资源类型
        get_resource_id: 获取资源ID的函数
        get_resource_name: 获取资源名称的函数
        capture_request: 是否捕获请求数据
        capture_response: 是否捕获响应数据
        capture_changes: 是否捕获数据变更
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # 提取参数
            db: Optional[Session] = None
            current_user: Optional[User] = None
            request: Optional[Request] = None
            
            # 从kwargs中提取常用参数
            for key, value in kwargs.items():
                if key == "db" and hasattr(value, "query"):
                    db = value
                elif key == "current_user" and hasattr(value, "id"):
                    current_user = value
                elif hasattr(value, "client") and hasattr(value, "url"):
                    request = value
            
            # 准备审计日志数据
            resource_id = None
            resource_name = None
            request_data = None
            old_values = None
            
            # 获取资源ID和名称
            if get_resource_id:
                try:
                    resource_id = get_resource_id(*args, **kwargs)
                except:
                    pass
            
            if get_resource_name:
                try:
                    resource_name = get_resource_name(*args, **kwargs)
                except:
                    pass
            
            # 捕获请求数据
            if capture_request:
                try:
                    # 提取请求体数据
                    for arg in args:
                        if hasattr(arg, 'model_dump'):
                            request_data = arg.model_dump()
                            break
                        elif hasattr(arg, 'dict'):
                            request_data = arg.dict()
                            break
                except:
                    pass
            
            # 如果需要捕获变更，先获取旧值
            if capture_changes and resource_id and db:
                try:
                    # 这里可以根据资源类型获取旧值
                    if resource_type == AuditResources.VENUE:
                        from src.models.venue import Venue
                        old_obj = db.query(Venue).filter(Venue.id == resource_id).first()
                        if old_obj:
                            old_values = {
                                "name": old_obj.name,
                                "type": old_obj.type,
                                "address": old_obj.address,
                                "capacity": old_obj.capacity,
                                "is_active": old_obj.is_active,
                                "status": old_obj.status
                            }
                except:
                    pass
            
            # 执行原函数
            error_message = None
            status_code = 200
            response_data = None
            
            try:
                result = await func(*args, **kwargs)
                
                # 捕获响应数据
                if capture_response and result:
                    try:
                        if hasattr(result, 'model_dump'):
                            response_data = result.model_dump()
                        elif hasattr(result, 'dict'):
                            response_data = result.dict()
                        elif isinstance(result, dict):
                            response_data = result
                    except:
                        pass
                
                return result
                
            except Exception as e:
                error_message = str(e)
                status_code = 500
                raise
            
            finally:
                # 记录审计日志
                if db:
                    try:
                        execution_time = int((time.time() - start_time) * 1000)
                        
                        # 获取新值（如果是更新操作）
                        new_values = None
                        if capture_changes and resource_id and action == AuditActions.UPDATE:
                            try:
                                if resource_type == AuditResources.VENUE:
                                    from src.models.venue import Venue
                                    new_obj = db.query(Venue).filter(Venue.id == resource_id).first()
                                    if new_obj:
                                        new_values = {
                                            "name": new_obj.name,
                                            "type": new_obj.type,
                                            "address": new_obj.address,
                                            "capacity": new_obj.capacity,
                                            "is_active": new_obj.is_active,
                                            "status": new_obj.status
                                        }
                            except:
                                pass
                        
                        # 获取客户端信息
                        ip_address = None
                        user_agent = None
                        endpoint = func.__name__
                        method = "POST"  # 默认值，实际应该从request获取
                        
                        if request:
                            try:
                                ip_address = getattr(request.client, 'host', None) if hasattr(request, 'client') else None
                                user_agent = request.headers.get('user-agent')
                                endpoint = str(request.url.path) if hasattr(request, 'url') else func.__name__
                                method = request.method if hasattr(request, 'method') else "POST"
                            except:
                                pass
                        
                        AuditService.log_operation(
                            db=db,
                            user=current_user,
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
                    except Exception as audit_error:
                        logger.error(f"记录审计日志失败: {audit_error}")
        
        return wrapper
    return decorator


# 便捷的审计装饰器
def audit_venue_create():
    """审计场地创建"""
    return audit_operation(
        action=AuditActions.CREATE,
        resource_type=AuditResources.VENUE,
        capture_request=True,
        capture_response=True
    )

def audit_venue_update():
    """审计场地更新"""
    return audit_operation(
        action=AuditActions.UPDATE,
        resource_type=AuditResources.VENUE,
        get_resource_id=lambda *args, **kwargs: kwargs.get('venue_id'),
        capture_request=True,
        capture_changes=True
    )

def audit_venue_delete():
    """审计场地删除"""
    return audit_operation(
        action=AuditActions.DELETE,
        resource_type=AuditResources.VENUE,
        get_resource_id=lambda *args, **kwargs: kwargs.get('venue_id'),
        capture_changes=True
    )

def audit_venue_read():
    """审计场地查看"""
    return audit_operation(
        action=AuditActions.READ,
        resource_type=AuditResources.VENUE,
        capture_request=False,
        capture_response=False
    )