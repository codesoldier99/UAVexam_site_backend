from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ...config.database import get_db
from ...models.user import User, UserRole
from ...models.institution import Institution
from ...schemas.institution import InstitutionCreate, InstitutionUpdate, InstitutionResponse
from ...services.auth_service import AuthService

router = APIRouter()

@router.get("/institutions", response_model=List[InstitutionResponse])
async def get_institutions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取机构列表"""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        query = db.query(Institution)
        
        # 搜索过滤
        if search:
            query = query.filter(Institution.name.contains(search))
        
        # 状态过滤
        if is_active is not None:
            query = query.filter(Institution.is_active == is_active)
        
        institutions = query.offset(skip).limit(limit).all()
        return institutions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取机构列表失败: {str(e)}")

@router.get("/institutions/{institution_id}", response_model=InstitutionResponse)
async def get_institution(
    institution_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取机构详情"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        institution = db.query(Institution).filter(Institution.id == institution_id).first()
        if not institution:
            raise HTTPException(status_code=404, detail="机构不存在")
        
        # 权限检查
        if current_user.role == UserRole.ADMIN and current_user.institution_id != institution_id:
            raise HTTPException(status_code=403, detail="无权访问此机构")
        
        return institution
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取机构详情失败: {str(e)}")

@router.get("/institutions/statistics")
async def get_institution_statistics(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取机构统计信息"""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        total_institutions = db.query(Institution).count()
        active_institutions = db.query(Institution).filter(Institution.is_active == True).count()
        
        return {
            "total_institutions": total_institutions,
            "active_institutions": active_institutions,
            "inactive_institutions": total_institutions - active_institutions
        }
    except Exception as e:
        # 如果查询失败，返回默认统计
        return {
            "total_institutions": 0,
            "active_institutions": 0,
            "inactive_institutions": 0
        }