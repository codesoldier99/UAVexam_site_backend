"""
RBAC权限控制核心模块
根据需求文档定义的5种角色和权限体系
"""
from enum import Enum
from typing import List, Dict, Any
from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.session import get_async_session
from src.db.models import User
from src.auth.fastapi_users_config import current_active_user

class UserRole(str, Enum):
    """用户角色枚举"""
    SUPER_ADMIN = "super_admin"        # 超级管理员
    EXAM_ADMIN = "exam_admin"          # 考务管理员  
    INSTITUTION_USER = "institution_user"  # 机构用户
    STAFF = "staff"                    # 考务人员
    CANDIDATE = "candidate"            # 考生

class Permission(str, Enum):
    """权限枚举"""
    # 用户管理权限
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    
    # 角色权限管理
    ROLE_MANAGE = "role:manage"
    PERMISSION_MANAGE = "permission:manage"
    
    # 基础信息配置权限
    EXAM_PRODUCT_MANAGE = "exam_product:manage"
    VENUE_MANAGE = "venue:manage"
    
    # 考生管理权限
    CANDIDATE_CREATE = "candidate:create"
    CANDIDATE_READ = "candidate:read"
    CANDIDATE_UPDATE = "candidate:update"
    CANDIDATE_DELETE = "candidate:delete"
    CANDIDATE_BATCH_IMPORT = "candidate:batch_import"
    
    # 考务排期权限
    SCHEDULE_CREATE = "schedule:create"
    SCHEDULE_READ = "schedule:read"
    SCHEDULE_UPDATE = "schedule:update"
    SCHEDULE_DELETE = "schedule:delete"
    SCHEDULE_BATCH_MANAGE = "schedule:batch_manage"
    
    # 签到权限
    CHECKIN_SCAN = "checkin:scan"
    CHECKIN_READ = "checkin:read"
    
    # 机构管理权限
    INSTITUTION_MANAGE = "institution:manage"
    INSTITUTION_READ = "institution:read"
    
    # 看板权限
    DASHBOARD_READ = "dashboard:read"

# 角色权限映射表
ROLE_PERMISSIONS: Dict[UserRole, List[Permission]] = {
    UserRole.SUPER_ADMIN: [
        # 超级管理员拥有所有权限
        Permission.USER_CREATE,
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,
        Permission.ROLE_MANAGE,
        Permission.PERMISSION_MANAGE,
        Permission.EXAM_PRODUCT_MANAGE,
        Permission.VENUE_MANAGE,
        Permission.CANDIDATE_CREATE,
        Permission.CANDIDATE_READ,
        Permission.CANDIDATE_UPDATE,
        Permission.CANDIDATE_DELETE,
        Permission.CANDIDATE_BATCH_IMPORT,
        Permission.SCHEDULE_CREATE,
        Permission.SCHEDULE_READ,
        Permission.SCHEDULE_UPDATE,
        Permission.SCHEDULE_DELETE,
        Permission.SCHEDULE_BATCH_MANAGE,
        Permission.CHECKIN_SCAN,
        Permission.CHECKIN_READ,
        Permission.INSTITUTION_MANAGE,
        Permission.INSTITUTION_READ,
        Permission.DASHBOARD_READ,
    ],
    
    UserRole.EXAM_ADMIN: [
        # 考务管理员：负责考务排期、监控全场
        Permission.EXAM_PRODUCT_MANAGE,
        Permission.VENUE_MANAGE,
        Permission.CANDIDATE_READ,
        Permission.SCHEDULE_CREATE,
        Permission.SCHEDULE_READ,
        Permission.SCHEDULE_UPDATE,
        Permission.SCHEDULE_DELETE,
        Permission.SCHEDULE_BATCH_MANAGE,
        Permission.CHECKIN_READ,
        Permission.INSTITUTION_READ,
        Permission.DASHBOARD_READ,
    ],
    
    UserRole.INSTITUTION_USER: [
        # 机构用户：为本机构学员报名，数据访问严格隔离
        Permission.CANDIDATE_CREATE,
        Permission.CANDIDATE_READ,
        Permission.CANDIDATE_UPDATE,
        Permission.CANDIDATE_BATCH_IMPORT,
        Permission.SCHEDULE_READ,
        Permission.DASHBOARD_READ,
    ],
    
    UserRole.STAFF: [
        # 考务人员：现场扫码签到
        Permission.CHECKIN_SCAN,
        Permission.CHECKIN_READ,
        Permission.DASHBOARD_READ,
    ],
    
    UserRole.CANDIDATE: [
        # 考生：查看信息和出示二维码
        Permission.SCHEDULE_READ,
        Permission.DASHBOARD_READ,
    ]
}

class RBACChecker:
    """RBAC权限检查器"""
    
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission
    
    async def __call__(
        self,
        current_user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
    ):
        """检查用户是否有指定权限"""
        # 获取用户角色
        user_role = await self._get_user_role(current_user, db)
        
        # 检查权限
        if not self._has_permission(user_role, self.required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足：需要 {self.required_permission.value} 权限"
            )
        
        return current_user
    
    async def _get_user_role(self, user: User, db: AsyncSession) -> UserRole:
        """获取用户角色"""
        # 通过role_id查询角色名称
        from src.models.role import Role
        result = await db.execute(select(Role).where(Role.id == user.role_id))
        role = result.scalar_one_or_none()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户角色不存在"
            )
        
        # 将角色名称转换为枚举
        try:
            return UserRole(role.name)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的角色：{role.name}"
            )
    
    def _has_permission(self, user_role: UserRole, permission: Permission) -> bool:
        """检查角色是否有指定权限"""
        role_permissions = ROLE_PERMISSIONS.get(user_role, [])
        return permission in role_permissions

# 权限检查装饰器工厂
def require_permission(permission: Permission):
    """权限检查装饰器工厂"""
    return RBACChecker(permission)

# 机构数据隔离检查器
class InstitutionDataChecker:
    """机构数据隔离检查器"""
    
    async def __call__(
        self,
        current_user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
    ):
        """检查机构用户的数据访问权限"""
        user_role = await self._get_user_role(current_user, db)
        
        # 机构用户必须有institution_id
        if user_role == UserRole.INSTITUTION_USER:
            if not current_user.institution_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="机构用户缺少机构关联"
                )
        
        return current_user
    
    async def _get_user_role(self, user: User, db: AsyncSession) -> UserRole:
        """获取用户角色"""
        from src.models.role import Role
        result = await db.execute(select(Role).where(Role.id == user.role_id))
        role = result.scalar_one_or_none()
        
        if role:
            try:
                return UserRole(role.name)
            except ValueError:
                pass
        
        return UserRole.CANDIDATE  # 默认为考生角色

# 机构数据隔离检查实例
check_institution_access = InstitutionDataChecker()

# 常用权限检查器实例
require_super_admin = require_permission(Permission.USER_CREATE)
require_exam_admin = require_permission(Permission.SCHEDULE_BATCH_MANAGE)
require_institution_user = require_permission(Permission.CANDIDATE_BATCH_IMPORT)
require_staff = require_permission(Permission.CHECKIN_SCAN)