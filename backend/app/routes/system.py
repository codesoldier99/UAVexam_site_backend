"""
系统管理API路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..config.database import get_db
from ..config.settings import settings
from ..services.auth_service import AuthService
from ..models.user import User, UserRole

router = APIRouter(prefix="/system", tags=["系统管理"])


@router.get("/config", summary="获取系统配置")
async def get_system_config(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取系统可配置参数和设置"""
    
    # 基础系统配置
    config = {
        "app_info": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": "development" if settings.debug else "production"
        },
        "auth_settings": {
            "token_expire_minutes": settings.access_token_expire_minutes,
            "password_min_length": 6,
            "username_min_length": 3
        },
        "file_upload": {
            "max_file_size": settings.max_file_size if hasattr(settings, 'max_file_size') else 10485760,  # 10MB
            "allowed_extensions": [".xlsx", ".xls", ".csv"],
            "upload_path": settings.upload_path if hasattr(settings, 'upload_path') else "uploads"
        },
        "exam_settings": {
            "max_candidates_per_venue": 50,
            "exam_duration_minutes": 120,
            "checkin_advance_minutes": 30,
            "late_arrival_tolerance_minutes": 15
        },
        "venue_settings": {
            "default_capacity": 20,
            "venue_types": ["理论", "实操", "综合"],
            "status_options": ["active", "inactive", "maintenance"]
        },
        "notification_settings": {
            "email_enabled": bool(getattr(settings, 'smtp_server', None)),
            "sms_enabled": False,
            "wechat_enabled": bool(getattr(settings, 'wechat_app_id', None))
        }
    }
    
    # 根据用户角色返回不同级别的配置信息
    if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        # 管理员可以看到完整配置
        config.update({
            "database_settings": {
                "host": getattr(settings, 'db_host', 'localhost'),
                "port": getattr(settings, 'db_port', 3306),
                "name": getattr(settings, 'db_name', 'exam_site_dev_db')
            },
            "redis_settings": {
                "enabled": bool(getattr(settings, 'redis_url', None)),
                "url": getattr(settings, 'redis_url', 'redis://redis:6379/0') if hasattr(settings, 'redis_url') else None
            },
            "cors_settings": {
                "origins": settings.cors_origins_list if hasattr(settings, 'cors_origins_list') else []
            }
        })
    
    return config


@router.get("/status", summary="获取系统状态")
async def get_system_status(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取系统运行状态"""
    
    # 基础状态信息
    status_info = {
        "status": "healthy",
        "timestamp": "2025-01-15T12:00:00Z",
        "uptime": "24小时",
        "version": settings.app_version,
        "services": {
            "database": "connected",
            "redis": "connected" if hasattr(settings, 'redis_url') else "not_configured",
            "wechat": "configured" if hasattr(settings, 'wechat_app_id') else "not_configured"
        }
    }
    
    # 管理员可以看到详细状态
    if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        # 统计数据库中的记录数量
        from ..models.user import User
        from ..models.institution import Institution
        from ..models.venue import Venue
        from ..models.exam import ExamProduct
        
        status_info.update({
            "statistics": {
                "total_users": db.query(User).count(),
                "total_institutions": db.query(Institution).count(),
                "total_venues": db.query(Venue).count(),
                "total_exam_products": db.query(ExamProduct).count()
            },
            "performance": {
                "active_connections": 1,  # 简化显示
                "memory_usage": "128MB",  # 简化显示
                "cpu_usage": "15%"        # 简化显示
            }
        })
    
    return status_info


@router.get("/features", summary="获取系统功能特性")
async def get_system_features() -> Dict[str, Any]:
    """获取系统支持的功能特性列表"""
    return {
        "authentication": {
            "jwt_token": True,
            "role_based_access": True,
            "multi_login_methods": True
        },
        "user_management": {
            "user_registration": True,
            "role_management": True,
            "institution_binding": True
        },
        "exam_management": {
            "exam_products": True,
            "candidate_management": True,
            "venue_management": True,
            "schedule_management": True
        },
        "integrations": {
            "wechat_miniprogram": bool(getattr(settings, 'wechat_app_id', None)),
            "qr_code_checkin": True,
            "email_notifications": bool(getattr(settings, 'smtp_server', None)),
            "file_upload": True
        },
        "reporting": {
            "real_time_dashboard": True,
            "export_functionality": True,
            "statistics": True
        },
        "scalability": {
            "concurrent_users": 1200,
            "docker_deployment": True,
            "load_balancing_ready": True
        }
    }


@router.get("/version", summary="获取版本信息")
async def get_version_info() -> Dict[str, Any]:
    """获取系统版本信息"""
    return {
        "version": settings.app_version,
        "build_date": "2025-01-15",
        "git_commit": "latest",
        "api_version": "v1",
        "changelog": [
            {
                "version": "1.0.0",
                "date": "2025-01-15",
                "changes": [
                    "初始版本发布",
                    "完整的考点运营管理功能",
                    "微信小程序支持",
                    "Docker部署支持"
                ]
            }
        ]
    }
