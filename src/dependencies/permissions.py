"""
权限控制依赖
实现基于角色的访问控制(RBAC)
"""

from functools import wraps
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from src.dependencies.get_current_user import get_current_user
from src.dependencies.get_db import get_db
from src.models.user import User

class VenuePermissions:
    """场地管理权限定义"""
    VIEW = "venue:read"      # 查看考场
    CREATE = "venue:create"  # 创建考场
    UPDATE = "venue:update"  # 更新考场
    DELETE = "venue:delete"  # 删除考场
    MANAGE = "venue:manage"  # 管理考场（批量操作）
    STATS = "venue:stats"    # 查看统计

class InstitutionPermissions:
    """机构管理权限定义"""
    VIEW = "institution:read"      # 查看机构
    CREATE = "institution:create"  # 创建机构
    UPDATE = "institution:update"  # 更新机构
    DELETE = "institution:delete"  # 删除机构
    MANAGE = "institution:manage"  # 管理机构

class UserRole:
    """用户角色定义"""
    SUPER_ADMIN = "super_admin"  # 超级管理员
    ADMIN = "admin"              # 管理员
    MANAGER = "manager"          # 经理
    OPERATOR = "operator"        # 操作员
    VIEWER = "viewer"            # 查看者

# 角色权限映射
ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN: [
        # 场地权限
        VenuePermissions.VIEW,
        VenuePermissions.CREATE,
        VenuePermissions.UPDATE,
        VenuePermissions.DELETE,
        VenuePermissions.MANAGE,
        VenuePermissions.STATS,
        # 机构权限
        InstitutionPermissions.VIEW,
        InstitutionPermissions.CREATE,
        InstitutionPermissions.UPDATE,
        InstitutionPermissions.DELETE,
        InstitutionPermissions.MANAGE,
    ],
    UserRole.ADMIN: [
        # 场地权限
        VenuePermissions.VIEW,
        VenuePermissions.CREATE,
        VenuePermissions.UPDATE,
        VenuePermissions.MANAGE,
        VenuePermissions.STATS,
        # 机构权限
        InstitutionPermissions.VIEW,
        InstitutionPermissions.CREATE,
        InstitutionPermissions.UPDATE,
        InstitutionPermissions.MANAGE,
    ],
    UserRole.MANAGER: [
        # 场地权限
        VenuePermissions.VIEW,
        VenuePermissions.CREATE,
        VenuePermissions.UPDATE,
        VenuePermissions.STATS,
        # 机构权限
        InstitutionPermissions.VIEW,
        InstitutionPermissions.UPDATE,
    ],
    UserRole.OPERATOR: [
        # 场地权限
        VenuePermissions.VIEW,
        VenuePermissions.UPDATE,
        # 机构权限
        InstitutionPermissions.VIEW,
    ],
    UserRole.VIEWER: [
        # 场地权限
        VenuePermissions.VIEW,
        # 机构权限
        InstitutionPermissions.VIEW,
    ],
}

def get_user_permissions(user: User, db: Session) -> List[str]:
    """获取用户权限列表"""
    from src.models.role import Role
    
    # 获取用户角色
    if hasattr(user, 'role_id') and user.role_id:
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if role:
            role_name = role.name.lower()
            # 映射数据库角色名到权限系统角色
            role_mapping = {
                'super_admin': UserRole.SUPER_ADMIN,
                'admin': UserRole.ADMIN,
                'manager': UserRole.MANAGER,
                'operator': UserRole.OPERATOR,
                'viewer': UserRole.VIEWER,
            }
            user_role = role_mapping.get(role_name, UserRole.VIEWER)
        else:
            user_role = UserRole.VIEWER
    else:
        user_role = UserRole.VIEWER
    
    return ROLE_PERMISSIONS.get(user_role, ROLE_PERMISSIONS[UserRole.VIEWER])

def check_permission(required_permission: str):
    """权限检查装饰器"""
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        user_permissions = get_user_permissions(current_user, db)
        
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要权限: {required_permission}"
            )
        
        return current_user
    
    return permission_checker

# 具体权限检查依赖
def require_venue_view():
    """需要查看考场权限"""
    return check_permission(VenuePermissions.VIEW)

def require_venue_create():
    """需要创建考场权限"""
    return check_permission(VenuePermissions.CREATE)

def require_venue_update():
    """需要更新考场权限"""
    return check_permission(VenuePermissions.UPDATE)

def require_venue_delete():
    """需要删除考场权限"""
    return check_permission(VenuePermissions.DELETE)

def require_venue_manage():
    """需要管理考场权限"""
    return check_permission(VenuePermissions.MANAGE)

def require_venue_stats():
    """需要查看统计权限"""
    return check_permission(VenuePermissions.STATS)

# 机构权限检查依赖
def require_institution_read():
    """需要查看机构权限"""
    return check_permission(InstitutionPermissions.VIEW)

def require_institution_create():
    """需要创建机构权限"""
    return check_permission(InstitutionPermissions.CREATE)

def require_institution_update():
    """需要更新机构权限"""
    return check_permission(InstitutionPermissions.UPDATE)

def require_institution_delete():
    """需要删除机构权限"""
    return check_permission(InstitutionPermissions.DELETE)

def require_institution_manage():
    """需要管理机构权限"""
    return check_permission(InstitutionPermissions.MANAGE)

def get_user_role_display(user: User, db: Session) -> str:
    """获取用户角色显示名称"""
    from src.models.role import Role
    
    if hasattr(user, 'role_id') and user.role_id:
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if role:
            return role.name
    return "查看者"