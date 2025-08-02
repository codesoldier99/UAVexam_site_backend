from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from src.dependencies.get_db import get_db
from src.dependencies.temp_permissions import (
    temp_exam_product_read, temp_exam_product_create,
    temp_exam_product_update, temp_exam_product_delete
)
from src.schemas.exam_product import ExamProductCreate, ExamProductRead, ExamProductUpdate, ExamProductStatus
from src.models.exam_product import ExamProduct
from src.models.user import User

router = APIRouter(
    prefix="/exam-products",
    tags=["exam_products"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ExamProductRead, status_code=status.HTTP_201_CREATED)
async def create_exam_product(
    exam_product: ExamProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(temp_exam_product_create)
):
    """创建考试产品"""
    # 检查产品名称是否已存在
    existing_product = db.query(ExamProduct).filter(ExamProduct.name == exam_product.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="考试产品名称已存在"
        )
    
    # 生成唯一的code
    if not exam_product.code:
        import time
        exam_product.code = f"PROD_{int(time.time())}"
    
    # 检查code是否已存在
    existing_code = db.query(ExamProduct).filter(ExamProduct.code == exam_product.code).first()
    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="考试产品代码已存在"
        )
    
    # 创建新考试产品
    new_product = ExamProduct(
        name=exam_product.name,
        description=exam_product.description,
        code=exam_product.code,
        category=exam_product.category,
        exam_type=exam_product.exam_type,
        exam_class=exam_product.exam_class,
        exam_level=exam_product.exam_level,
        duration_minutes=exam_product.duration_minutes,
        theory_pass_score=exam_product.theory_pass_score,
        practical_pass_score=exam_product.practical_pass_score,
        training_hours=exam_product.training_hours,
        price=exam_product.price,
        training_price=exam_product.training_price,
        theory_content=exam_product.theory_content,
        practical_content=exam_product.practical_content,
        requirements=exam_product.requirements,
        status=ExamProductStatus.active
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.get("/", response_model=List[ExamProductRead])
async def get_exam_products(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(temp_exam_product_read)
):
    """获取考试产品列表"""
    skip = (page - 1) * size
    exam_products = db.query(ExamProduct).offset(skip).limit(size).all()
    
    return exam_products


@router.get("/{exam_product_id}", response_model=ExamProductRead)
async def get_exam_product(
    exam_product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(temp_exam_product_read)
):
    """根据ID获取考试产品详情"""
    exam_product = db.query(ExamProduct).filter(ExamProduct.id == exam_product_id).first()
    if not exam_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考试产品不存在"
        )
    return exam_product


@router.put("/{exam_product_id}", response_model=ExamProductRead)
async def update_exam_product(
    exam_product_id: int,
    exam_product: ExamProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(temp_exam_product_update)
):
    """更新考试产品信息"""
    db_product = db.query(ExamProduct).filter(ExamProduct.id == exam_product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考试产品不存在"
        )
    
    # 检查名称是否重复
    if exam_product.name and exam_product.name != db_product.name:
        existing = db.query(ExamProduct).filter(
            ExamProduct.name == exam_product.name,
            ExamProduct.id != exam_product_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="考试产品名称已存在"
            )
    
    # 更新字段
    update_data = exam_product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    
    return db_product


@router.delete("/{exam_product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam_product(
    exam_product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(temp_exam_product_delete)
):
    """删除考试产品"""
    exam_product = db.query(ExamProduct).filter(ExamProduct.id == exam_product_id).first()
    if not exam_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考试产品不存在"
        )
    
    db.delete(exam_product)
    db.commit()
    
    return {"message": "考试产品删除成功"} 