"""
产业级认证依赖模块
统一使用 FastAPI-Users 认证系统
"""
from src.auth.fastapi_users_config import current_active_user, current_superuser

# 产业级认证依赖 - 直接使用 FastAPI-Users 的认证
get_current_user = current_active_user
get_current_active_user = current_active_user  
get_current_superuser = current_superuser

__all__ = [
    "get_current_user", 
    "get_current_active_user", 
    "get_current_superuser"
]