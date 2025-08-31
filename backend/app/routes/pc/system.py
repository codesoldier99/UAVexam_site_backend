"""
PC端系统管理接口
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from ...config.database import get_db
from ...models.user import User, UserRole
from ...models.checkin import CheckIn
from ...models.schedule import Schedule
from ...models.exam import ExamRegistration
from ...services.auth_service import AuthService

get_current_user = AuthService.get_current_user


router = APIRouter(prefix="/system", tags=["PC-系统管理"])

@router.get("/overview", summary="系统概览统计")
async def get_system_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取系统整体概览数据"""
    try:
        # 用户统计
        total_users = db.query(User).count()
        admin_users = db.query(User).filter(User.role.in_([UserRole.SUPER_ADMIN, UserRole.ADMIN])).count()
        candidate_users = db.query(User).filter(User.role == UserRole.CANDIDATE).count()
        
        # 考试统计
        total_schedules = db.query(Schedule).count()
        active_schedules = db.query(Schedule).filter(Schedule.status == "ACTIVE").count()
        
        # 报名统计
        total_registrations = db.query(ExamRegistration).count()
        confirmed_registrations = db.query(ExamRegistration).filter(
            ExamRegistration.status == "CONFIRMED"
        ).count()
        
        # 签到统计
        total_checkins = db.query(CheckIn).count()
        successful_checkins = db.query(CheckIn).filter(CheckIn.status == "SUCCESS").count()
        
        return {
            "code": 200,
            "message": "获取系统概览成功",
            "data": {
                "users": {
                    "total": total_users,
                    "admins": admin_users,
                    "candidates": candidate_users
                },
                "schedules": {
                    "total": total_schedules,
                    "active": active_schedules
                },
                "registrations": {
                    "total": total_registrations,
                    "confirmed": confirmed_registrations
                },
                "checkins": {
                    "total": total_checkins,
                    "successful": successful_checkins
                }
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取系统概览失败: {str(e)}",
            "data": {
                "users": {"total": 0, "admins": 0, "candidates": 0},
                "schedules": {"total": 0, "active": 0},
                "registrations": {"total": 0, "confirmed": 0},
                "checkins": {"total": 0, "successful": 0}
            }
        }

@router.get("/logs", summary="系统日志查询")
async def get_system_logs(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    level: Optional[str] = Query(None, description="日志级别"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取系统日志（模拟数据）"""
    try:
        # 模拟日志数据
        logs = [
            {
                "id": i,
                "timestamp": "2024-01-01 12:00:00",
                "level": "INFO" if i % 3 == 0 else "ERROR" if i % 5 == 0 else "WARN",
                "module": "auth" if i % 2 == 0 else "checkin",
                "message": f"系统操作日志 {i}",
                "user_id": current_user.id if i % 4 == 0 else None
            }
            for i in range((page - 1) * size + 1, page * size + 1)
        ]
        
        if level:
            logs = [log for log in logs if log["level"] == level.upper()]
        
        return {
            "code": 200,
            "message": "获取系统日志成功",
            "data": {
                "items": logs,
                "total": 1000,  # 模拟总数
                "page": page,
                "size": size
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取系统日志失败: {str(e)}",
            "data": {"items": [], "total": 0, "page": page, "size": size}
        }

@router.post("/backup", summary="数据备份")
async def create_backup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建数据备份"""
    try:
        # 检查权限
        if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 模拟备份操作
        backup_id = f"backup_{current_user.id}_{int(__import__('time').time())}"
        
        return {
            "code": 200,
            "message": "数据备份创建成功",
            "data": {
                "backup_id": backup_id,
                "created_at": "2024-01-01 12:00:00",
                "size": "10.5MB",
                "status": "completed"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "code": 500,
            "message": f"创建数据备份失败: {str(e)}",
            "data": None
        }

@router.get("/config", summary="系统配置")
async def get_system_config(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取系统配置"""
    try:
        # 检查权限
        if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        return {
            "code": 200,
            "message": "获取系统配置成功",
            "data": {
                "system": {
                    "name": "无人机考试管理系统",
                    "version": "1.0.0",
                    "environment": "production"
                },
                "database": {
                    "type": "MySQL",
                    "version": "8.0",
                    "status": "connected"
                },
                "features": {
                    "auto_checkin": True,
                    "manual_checkin": True,
                    "batch_operations": True,
                    "data_export": True
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取系统配置失败: {str(e)}",
            "data": None
        }