from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.dependencies.get_db import get_db
from src.dependencies.permissions import (
    require_institution_read, require_institution_create, 
    require_institution_update, require_institution_delete
)
from src.schemas.institution import (
    InstitutionCreate, InstitutionRead, InstitutionUpdate, InstitutionStatus
)
from src.institutions.models import Institution
from src.models.user import User

router = APIRouter(
    prefix="/institutions",
    tags=["institutions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=InstitutionRead, status_code=status.HTTP_201_CREATED)
async def create_institution(
    institution: InstitutionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_institution_create)
):
    """创建新机构"""
    # 检查机构名称是否已存在
    existing_institution = db.query(Institution).filter(Institution.name == institution.name).first()
    if existing_institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="机构名称已存在"
        )
    
    # 创建新机构
    new_institution = Institution(
        name=institution.name,
        contact_person=institution.contact_person,
        phone=institution.phone,
        status=InstitutionStatus.active
    )
    
    db.add(new_institution)
    db.commit()
    db.refresh(new_institution)
    
    return new_institution


@router.get("/")
async def get_institutions(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    status_filter: Optional[str] = Query(None, description="状态过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_institution_read)
):
    """获取机构列表（支持搜索和过滤）"""
    query = db.query(Institution)
    
    # 搜索过滤
    if search:
        query = query.filter(Institution.name.contains(search))
    
    # 状态过滤
    if status_filter:
        query = query.filter(Institution.status == status_filter)
    
    # 计算总数
    total = query.count()
    
    # 分页
    skip = (page - 1) * size
    institutions = query.offset(skip).limit(size).all()
    
    # 转换为响应格式
    institution_list = []
    for institution in institutions:
        institution_dict = {
            "id": institution.id,
            "name": institution.name,
            "code": institution.code,
            "contact_person": institution.contact_person,
            "phone": institution.phone,
            "email": institution.email,
            "address": institution.address,
            "description": institution.description,
            "status": institution.status,
            "license_number": institution.license_number,
            "business_scope": institution.business_scope,
            "created_at": institution.created_at.isoformat() if institution.created_at else None,
            "updated_at": institution.updated_at.isoformat() if institution.updated_at else None
        }
        institution_list.append(institution_dict)
    
    # 计算分页信息
    total_pages = (total + size - 1) // size
    
    return {
        "message": "机构列表获取成功",
        "data": institution_list,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }


@router.get("/stats")
async def get_institution_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_institution_read)
):
    """获取机构统计信息"""
    total_institutions = db.query(Institution).count()
    active_institutions = db.query(Institution).filter(Institution.status == InstitutionStatus.active).count()
    inactive_institutions = db.query(Institution).filter(Institution.status == InstitutionStatus.inactive).count()
    
    return {
        "total_institutions": total_institutions,
        "active_institutions": active_institutions,
        "inactive_institutions": inactive_institutions
    }


@router.get("/{institution_id}", response_model=InstitutionRead)
async def get_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_institution_read)
):
    """根据ID获取机构详情"""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    return institution


@router.put("/{institution_id}", response_model=InstitutionRead)
async def update_institution(
    institution_id: int,
    institution: InstitutionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_institution_update)
):
    """更新机构信息"""
    db_institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not db_institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    
    # 检查名称是否重复
    if institution.name and institution.name != db_institution.name:
        existing = db.query(Institution).filter(
            Institution.name == institution.name,
            Institution.id != institution_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="机构名称已存在"
            )
    
    # 更新字段
    update_data = institution.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_institution, field, value)
    
    db.commit()
    db.refresh(db_institution)
    
    return db_institution


@router.patch("/{institution_id}/status")
async def update_institution_status(
    institution_id: int,
    status: InstitutionStatus = Query(..., description="新状态：active/inactive"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_institution_update)
):
    """更新机构状态"""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    
    institution.status = status
    db.commit()
    db.refresh(institution)
    
    return {"message": "机构状态更新成功", "institution_id": institution_id, "status": status}


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_institution_delete)
):
    """删除机构"""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    
    db.delete(institution)
    db.commit()
    
    return {"message": "机构删除成功"} 