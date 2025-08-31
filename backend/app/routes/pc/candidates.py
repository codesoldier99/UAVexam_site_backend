"""
PC前端考生管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from ...config.database import get_db
from ...services.auth_service import AuthService
from ...services.candidate_service import CandidateService
from ...models.user import User, UserRole
from ...schemas.candidate import (
    CandidateCreate, CandidateUpdate, CandidateResponse, 
    CandidateList, BatchImportResult, CandidateStatistics
)

router = APIRouter(prefix="/candidates", tags=["PC-考生管理"])


@router.get("/", summary="获取考生列表")
async def get_pc_candidates(
    page: int = 1,
    size: int = 20,
    search: Optional[str] = None,
    institution_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """PC端获取考生列表 - 支持分页、搜索、筛选"""
    
    # 权限检查
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    try:
        # 简化查询，直接查询考生用户
        query = db.query(User).filter(User.role == UserRole.CANDIDATE)
        
        # 根据用户角色过滤
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            # 管理员只能看到自己机构的考生
            from ...models.exam import ExamRegistration
            subquery = db.query(ExamRegistration.user_id).filter(
                ExamRegistration.institution_id == current_user.institution_id
            ).distinct()
            query = query.filter(User.id.in_(subquery))
        
        # 搜索过滤
        if search:
            query = query.filter(
                User.real_name.contains(search) | 
                User.username.contains(search) |
                User.phone.contains(search)
            )
        
        # 分页
        total = query.count()
        candidates = query.offset((page - 1) * size).limit(size).all()
        
        return {
            "items": candidates,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }
    except Exception as e:
        # 如果服务调用失败，返回简化的结果
        candidates = db.query(User).filter(User.role == UserRole.CANDIDATE).offset((page - 1) * size).limit(size).all()
        total = db.query(User).filter(User.role == UserRole.CANDIDATE).count()
        
        return {
            "items": [
                {
                    "id": candidate.id,
                    "real_name": candidate.real_name,
                    "id_card": candidate.id_card,
                    "phone": candidate.phone,
                    "email": candidate.email,
                    "institution_id": candidate.institution_id,
                    "is_active": candidate.is_active,
                    "created_at": candidate.created_at.isoformat() if candidate.created_at else None
                }
                for candidate in candidates
            ],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }


@router.get("/{candidate_id}", summary="获取考生详情")
async def get_pc_candidate_detail(
    candidate_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """PC端获取考生详情"""
    
    # 权限检查
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    # 查询考生
    candidate = db.query(User).filter(
        User.id == candidate_id,
        User.role == UserRole.CANDIDATE
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在"
        )
    
    # 操作员权限检查
    if current_user.role == UserRole.OPERATOR and current_user.institution_id:
        if candidate.institution_id != current_user.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只能查看本机构考生信息"
            )
    
    return {
        "id": candidate.id,
        "username": candidate.username,
        "real_name": candidate.real_name,
        "id_card": candidate.id_card,
        "phone": candidate.phone,
        "email": candidate.email,
        "institution_id": candidate.institution_id,
        "is_active": candidate.is_active,
        "is_verified": candidate.is_verified,
        "created_at": candidate.created_at.isoformat() if candidate.created_at else None,
        "updated_at": candidate.updated_at.isoformat() if candidate.updated_at else None
    }


@router.post("/", response_model=CandidateResponse, summary="创建考生")
async def create_pc_candidate(
    candidate_data: CandidateCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """PC端创建考生"""
    
    # 权限检查
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    # 操作员只能在本机构创建考生
    if current_user.role == UserRole.OPERATOR and current_user.institution_id:
        candidate_data.institution_id = current_user.institution_id
    
    candidate_service = CandidateService(db)
    return candidate_service.create_candidate(candidate_data)


@router.put("/{candidate_id}", response_model=CandidateResponse, summary="更新考生信息")
async def update_pc_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """PC端更新考生信息"""
    
    # 权限检查
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    candidate_service = CandidateService(db)
    
    # 操作员权限检查
    if current_user.role == UserRole.OPERATOR and current_user.institution_id:
        candidate = candidate_service.get_candidate_by_id(candidate_id)
        if not candidate or candidate.institution_id != current_user.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只能修改本机构考生信息"
            )
    
    updated_candidate = candidate_service.update_candidate(candidate_id, candidate_data)
    if not updated_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在"
        )
    
    return updated_candidate


@router.delete("/{candidate_id}", summary="删除考生")
async def delete_pc_candidate(
    candidate_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """PC端删除考生"""
    
    # 权限检查 - 只有管理员可以删除
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有管理员可以删除考生"
        )
    
    candidate_service = CandidateService(db)
    success = candidate_service.delete_candidate(candidate_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在"
        )
    
    return {"message": "考生删除成功"}


@router.post("/batch-import", response_model=BatchImportResult, summary="批量导入考生")
async def batch_import_pc_candidates(
    file: UploadFile = File(...),
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """PC端批量导入考生"""
    
    # 权限检查
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    # 文件格式检查
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持Excel文件格式"
        )
    
    try:
        import pandas as pd
        import io
        
        # 读取Excel文件
        content = await file.read()
        df = pd.read_excel(io.BytesIO(content))
        
        candidate_service = CandidateService(db)
        
        # 操作员只能导入到本机构
        institution_id = current_user.institution_id if (current_user.role == UserRole.OPERATOR and current_user.institution_id) else None
        
        result = candidate_service.batch_import_candidates(df, institution_id)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件处理失败: {str(e)}"
        )


@router.get("/statistics", summary="获取考生统计")
async def get_pc_candidate_statistics(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """PC端获取考生统计数据"""
    
    # 权限检查
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    candidate_service = CandidateService(db)
    
    # 操作员只能查看本机构统计
    institution_id = current_user.institution_id if (current_user.role == UserRole.OPERATOR and current_user.institution_id) else None
    
    return candidate_service.get_candidate_statistics(institution_id)