from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import pandas as pd
from io import BytesIO
from app.api.deps import get_async_db, get_current_institution_user, get_current_exam_admin
from app.models.candidate import Candidate, CandidateStatus
from app.models.institution import Institution
from app.models.exam import ExamProduct
from app.schemas.candidate import (
    CandidateCreate, 
    Candidate as CandidateSchema,
    CandidateBatchImport,
    CandidateWithDetails
)

router = APIRouter()

@router.post("/", response_model=CandidateSchema)
async def create_candidate(
    candidate: CandidateCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_institution_user)
):
    """创建单个考生"""
    # 检查身份证是否已存在
    existing = await db.execute(
        select(Candidate).where(Candidate.id_card == candidate.id_card)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID card already registered"
        )
    
    # 如果是机构用户，只能为自己机构添加考生
    if not current_user.is_superuser and current_user.institution_id:
        candidate.institution_id = current_user.institution_id
    
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    await db.commit()
    await db.refresh(db_candidate)
    return db_candidate

@router.post("/batch", response_model=List[CandidateSchema])
async def batch_import_candidates(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_institution_user)
):
    """批量导入考生（Excel文件）"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Excel files are supported"
        )
    
    # 读取Excel文件
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    
    # 验证必需列
    required_columns = ['姓名', '身份证号', '考试产品']
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Excel must contain columns: {required_columns}"
        )
    
    created_candidates = []
    errors = []
    
    for idx, row in df.iterrows():
        try:
            # 查找考试产品
            exam_product = await db.execute(
                select(ExamProduct).where(ExamProduct.name == row['考试产品'])
            )
            exam_product = exam_product.scalar_one_or_none()
            if not exam_product:
                errors.append(f"Row {idx+2}: Exam product '{row['考试产品']}' not found")
                continue
            
            # 检查身份证是否已存在
            existing = await db.execute(
                select(Candidate).where(Candidate.id_card == row['身份证号'])
            )
            if existing.scalar_one_or_none():
                errors.append(f"Row {idx+2}: ID card already registered")
                continue
            
            # 创建考生
            candidate = Candidate(
                name=row['姓名'],
                id_card=row['身份证号'],
                phone=row.get('电话'),
                email=row.get('邮箱'),
                institution_id=current_user.institution_id if current_user.institution_id else row.get('机构ID', 1),
                exam_product_id=exam_product.id
            )
            db.add(candidate)
            created_candidates.append(candidate)
            
        except Exception as e:
            errors.append(f"Row {idx+2}: {str(e)}")
    
    if created_candidates:
        await db.commit()
        for candidate in created_candidates:
            await db.refresh(candidate)
    
    if errors:
        raise HTTPException(
            status_code=status.HTTP_207_MULTI_STATUS,
            detail={
                "created": len(created_candidates),
                "errors": errors
            }
        )
    
    return created_candidates

@router.get("/", response_model=List[CandidateWithDetails])
async def list_candidates(
    skip: int = 0,
    limit: int = 100,
    institution_id: Optional[int] = None,
    status: Optional[CandidateStatus] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_institution_user)
):
    """获取考生列表"""
    query = select(Candidate)
    
    # 机构用户只能看到自己机构的考生
    if not current_user.is_superuser and current_user.institution_id:
        query = query.where(Candidate.institution_id == current_user.institution_id)
    elif institution_id:
        query = query.where(Candidate.institution_id == institution_id)
    
    if status:
        query = query.where(Candidate.status == status)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    candidates = result.scalars().all()
    
    # 添加关联信息
    detailed_candidates = []
    for candidate in candidates:
        # 获取机构名称
        inst = await db.execute(
            select(Institution).where(Institution.id == candidate.institution_id)
        )
        institution = inst.scalar_one_or_none()
        
        # 获取考试产品名称
        prod = await db.execute(
            select(ExamProduct).where(ExamProduct.id == candidate.exam_product_id)
        )
        product = prod.scalar_one_or_none()
        
        detailed = CandidateWithDetails(
            **candidate.__dict__,
            institution_name=institution.name if institution else None,
            exam_product_name=product.name if product else None
        )
        detailed_candidates.append(detailed)
    
    return detailed_candidates

@router.get("/{candidate_id}", response_model=CandidateWithDetails)
async def get_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_institution_user)
):
    """获取单个考生信息"""
    result = await db.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # 机构用户只能查看自己机构的考生
    if not current_user.is_superuser and current_user.institution_id:
        if candidate.institution_id != current_user.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this candidate"
            )
    
    # 获取关联信息
    inst = await db.execute(
        select(Institution).where(Institution.id == candidate.institution_id)
    )
    institution = inst.scalar_one_or_none()
    
    prod = await db.execute(
        select(ExamProduct).where(ExamProduct.id == candidate.exam_product_id)
    )
    product = prod.scalar_one_or_none()
    
    return CandidateWithDetails(
        **candidate.__dict__,
        institution_name=institution.name if institution else None,
        exam_product_name=product.name if product else None
    )