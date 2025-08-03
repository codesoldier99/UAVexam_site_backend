from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from src.db.session import get_async_session
from src.models.permission import Permission, RolePermission
from src.schemas.permission import PermissionCreate, PermissionUpdate, PermissionRead, RolePermissionCreate, RolePermissionRead
from src.auth.fastapi_users_config import current_active_user
from src.db.models import User

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("/", response_model=List[PermissionRead])
async def get_permissions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """获取权限列表"""
    result = await db.execute(
        select(Permission).offset(skip).limit(limit)
    )
    permissions = result.scalars().all()
    return permissions


@router.get("/{permission_id}", response_model=PermissionRead)
async def get_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """根据ID获取权限"""
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    permission = result.scalar_one_or_none()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    return permission


@router.post("/", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """创建权限"""
    # 检查权限名是否已存在
    result = await db.execute(select(Permission).where(Permission.name == permission_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限名已存在"
        )
    
    permission = Permission(**permission_data.model_dump())
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    return permission


@router.put("/{permission_id}", response_model=PermissionRead)
async def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """更新权限"""
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    permission = result.scalar_one_or_none()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    # 检查权限名是否已被其他权限使用
    if permission_data.name and permission_data.name != permission.name:
        result = await db.execute(select(Permission).where(Permission.name == permission_data.name))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="权限名已存在"
            )
    
    # 更新字段
    for field, value in permission_data.model_dump(exclude_unset=True).items():
        setattr(permission, field, value)
    
    await db.commit()
    await db.refresh(permission)
    return permission


@router.delete("/{permission_id}")
async def delete_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """删除权限"""
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    permission = result.scalar_one_or_none()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    await db.delete(permission)
    await db.commit()
    return {"message": "权限删除成功"}


@router.get("/roles/{role_id}/permissions", response_model=List[PermissionRead])
async def get_role_permissions(
    role_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """获取角色的权限列表"""
    from sqlalchemy.orm import joinedload
    result = await db.execute(
        select(Permission)
        .join(RolePermission)
        .where(RolePermission.role_id == role_id)
    )
    permissions = result.scalars().all()
    return permissions


@router.post("/roles/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """为角色分配权限"""
    # 检查是否已存在
    result = await db.execute(
        select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色已拥有该权限"
        )
    
    role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
    db.add(role_permission)
    await db.commit()
    return {"message": "权限分配成功"}


@router.delete("/roles/{role_id}/permissions/{permission_id}")
async def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """从角色中移除权限"""
    result = await db.execute(
        select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        )
    )
    role_permission = result.scalar_one_or_none()
    if not role_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色权限关系不存在"
        )
    
    await db.delete(role_permission)
    await db.commit()
    return {"message": "权限移除成功"}