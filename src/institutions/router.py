from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.dependencies.get_db import get_db
from src.institutions.schemas import InstitutionCreate, InstitutionRead, InstitutionUpdate
from src.institutions.service import InstitutionService

router = APIRouter(
    prefix="/institutions",
    tags=["institutions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=InstitutionRead, status_code=status.HTTP_201_CREATED)
def create_institution(
    institution: InstitutionCreate,
    db: Session = Depends(get_db)
):
    """创建新机构"""
    # 检查机构名称是否已存在
    existing_institution = InstitutionService.get_by_name(db, institution.name)
    if existing_institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="机构名称已存在"
        )
    
    return InstitutionService.create(db, institution)


@router.get("/", response_model=List[InstitutionRead])
def get_institutions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取机构列表"""
    return InstitutionService.get_multi(db, skip=skip, limit=limit)


@router.get("/{institution_id}", response_model=InstitutionRead)
def get_institution(
    institution_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取机构详情"""
    institution = InstitutionService.get(db, institution_id)
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    return institution


@router.put("/{institution_id}", response_model=InstitutionRead)
def update_institution(
    institution_id: int,
    institution: InstitutionUpdate,
    db: Session = Depends(get_db)
):
    """更新机构信息"""
    updated_institution = InstitutionService.update(db, institution_id, institution)
    if not updated_institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    return updated_institution


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db)
):
    """删除机构"""
    success = InstitutionService.delete(db, institution_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        ) 