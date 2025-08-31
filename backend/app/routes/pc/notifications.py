"""
PC端通知管理接口
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from ...config.database import get_db
from ...models.user import User, UserRole
from ...services.auth_service import AuthService

get_current_user = AuthService.get_current_user


router = APIRouter(prefix="/notifications", tags=["PC-通知管理"])

@router.get("", summary="获取通知列表")
async def get_notifications(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="通知状态"),
    type: Optional[str] = Query(None, description="通知类型"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取通知列表"""
    try:
        # 模拟通知数据
        notifications = []
        for i in range((page - 1) * size + 1, page * size + 1):
            notification = {
                "id": i,
                "title": f"系统通知 {i}",
                "content": f"这是第 {i} 条系统通知内容",
                "type": "SYSTEM" if i % 3 == 0 else "EXAM" if i % 2 == 0 else "MAINTENANCE",
                "status": "SENT" if i % 4 != 0 else "DRAFT",
                "target_users": "ALL" if i % 5 == 0 else "CANDIDATES",
                "created_at": "2024-01-01 12:00:00",
                "sent_at": "2024-01-01 12:05:00" if i % 4 != 0 else None,
                "read_count": i * 10 if i % 4 != 0 else 0,
                "total_recipients": 100
            }
            
            # 应用过滤条件
            if status and notification["status"] != status.upper():
                continue
            if type and notification["type"] != type.upper():
                continue
                
            notifications.append(notification)
        
        return {
            "code": 200,
            "message": "获取通知列表成功",
            "data": {
                "items": notifications,
                "total": 500,  # 模拟总数
                "page": page,
                "size": size
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取通知列表失败: {str(e)}",
            "data": {"items": [], "total": 0, "page": page, "size": size}
        }

@router.post("", summary="创建通知")
async def create_notification(
    notification_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建新通知"""
    try:
        # 检查权限
        if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 模拟创建通知
        notification_id = int(__import__('time').time())
        
        return {
            "code": 200,
            "message": "创建通知成功",
            "data": {
                "id": notification_id,
                "title": notification_data.get("title"),
                "content": notification_data.get("content"),
                "type": notification_data.get("type", "SYSTEM"),
                "status": "DRAFT",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": current_user.username
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "code": 500,
            "message": f"创建通知失败: {str(e)}",
            "data": None
        }

@router.put("/{notification_id}", summary="更新通知")
async def update_notification(
    notification_id: int,
    notification_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新通知信息"""
    try:
        # 检查权限
        if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        return {
            "code": 200,
            "message": "更新通知成功",
            "data": {
                "id": notification_id,
                "title": notification_data.get("title"),
                "content": notification_data.get("content"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "code": 500,
            "message": f"更新通知失败: {str(e)}",
            "data": None
        }

@router.post("/{notification_id}/send", summary="发送通知")
async def send_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """发送通知"""
    try:
        # 检查权限
        if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        return {
            "code": 200,
            "message": "通知发送成功",
            "data": {
                "notification_id": notification_id,
                "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "recipients_count": 150,
                "status": "SENT"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "code": 500,
            "message": f"发送通知失败: {str(e)}",
            "data": None
        }

@router.delete("/{notification_id}", summary="删除通知")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除通知"""
    try:
        # 检查权限
        if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        return {
            "code": 200,
            "message": "删除通知成功",
            "data": {"notification_id": notification_id}
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "code": 500,
            "message": f"删除通知失败: {str(e)}",
            "data": None
        }

@router.get("/statistics", summary="通知统计")
async def get_notification_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取通知统计数据"""
    try:
        return {
            "code": 200,
            "message": "获取通知统计成功",
            "data": {
                "total_notifications": 125,
                "sent_notifications": 100,
                "draft_notifications": 25,
                "total_recipients": 5000,
                "avg_read_rate": 75.5,
                "by_type": [
                    {"type": "SYSTEM", "count": 50, "read_rate": 80.2},
                    {"type": "EXAM", "count": 60, "read_rate": 72.8},
                    {"type": "MAINTENANCE", "count": 15, "read_rate": 68.5}
                ]
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取通知统计失败: {str(e)}",
            "data": {
                "total_notifications": 0, "sent_notifications": 0, "draft_notifications": 0,
                "total_recipients": 0, "avg_read_rate": 0, "by_type": []
            }
        }