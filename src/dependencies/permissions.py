from typing import List
from fastapi import Depends, HTTPException, status
from src.auth.fastapi_users_config import current_active_user
from src.models.user import User

def require_permission(permission_name: str):
    """
    权限依赖项
    
    Args:
        permission_name: 需要的权限名称
        
    Returns:
        依赖函数
    """
    async def permission_dependency(user: User = Depends(current_active_user)):
        # 获取用户权限列表
        from src.auth.fastapi_users_config import UserManager
        user_manager = UserManager(None)  # 临时创建实例来调用方法
        permissions = await user_manager.get_user_permissions(user)
        
        # 检查是否有超级管理员权限
        if "admin:all" in permissions:
            return user
            
        # 检查是否有特定权限
        if permission_name in permissions:
            return user
            
        # 没有权限，抛出403错误
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"权限不足，需要权限: {permission_name}"
        )
    
    return permission_dependency

def require_any_permission(permission_names: List[str]):
    """
    需要任意一个权限的依赖项
    
    Args:
        permission_names: 权限名称列表
        
    Returns:
        依赖函数
    """
    async def permission_dependency(user: User = Depends(current_active_user)):
        from src.auth.fastapi_users_config import UserManager
        user_manager = UserManager(None)
        permissions = await user_manager.get_user_permissions(user)
        
        # 检查是否有超级管理员权限
        if "admin:all" in permissions:
            return user
            
        # 检查是否有任意一个所需权限
        for permission in permission_names:
            if permission in permissions:
                return user
                
        # 没有权限，抛出403错误
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"权限不足，需要以下权限之一: {', '.join(permission_names)}"
        )
    
    return permission_dependency

def require_all_permissions(permission_names: List[str]):
    """
    需要所有权限的依赖项
    
    Args:
        permission_names: 权限名称列表
        
    Returns:
        依赖函数
    """
    async def permission_dependency(user: User = Depends(current_active_user)):
        from src.auth.fastapi_users_config import UserManager
        user_manager = UserManager(None)
        permissions = await user_manager.get_user_permissions(user)
        
        # 检查是否有超级管理员权限
        if "admin:all" in permissions:
            return user
            
        # 检查是否有所有所需权限
        for permission in permission_names:
            if permission not in permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"权限不足，缺少权限: {permission}"
                )
        
        return user
    
    return permission_dependency

# 预定义的权限依赖
require_user_read = require_permission("user:read")
require_user_write = require_permission("user:write")
require_user_delete = require_permission("user:delete")

# 机构管理权限
require_institution_read = require_permission("institution:read")
require_institution_create = require_permission("institution:create")
require_institution_update = require_permission("institution:update")
require_institution_delete = require_permission("institution:delete")

# 考试产品管理权限
require_exam_product_read = require_permission("exam_product:read")
require_exam_product_create = require_permission("exam_product:create")
require_exam_product_update = require_permission("exam_product:update")
require_exam_product_delete = require_permission("exam_product:delete")

# 考场资源管理权限
require_venue_read = require_permission("venue:read")
require_venue_create = require_permission("venue:create")
require_venue_update = require_permission("venue:update")
require_venue_delete = require_permission("venue:delete")

# 考试管理权限
require_exam_read = require_permission("exam:read")
require_exam_write = require_permission("exam:write")
require_exam_delete = require_permission("exam:delete")

# 管理员权限
require_admin = require_permission("admin:all") 