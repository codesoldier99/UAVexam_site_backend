"""
考生管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import io

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..services.candidate_service import CandidateService
from ..models.user import User, UserRole
from ..schemas.candidate import (
    CandidateCreate, CandidateUpdate, CandidateResponse, 
    CandidateList, BatchImportResult, CandidateStatistics
)

router = APIRouter(prefix="/candidates", tags=["考生管理"])


@router.get("/", response_model=CandidateList, summary="获取考生列表")
async def get_candidates(
    page: int = 1,
    size: int = 20,
    search: Optional[str] = None,
    institution_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """分页获取考生列表，支持搜索和筛选"""
    candidate_service = CandidateService(db)
    
    # 计算跳过的记录数
    skip = (page - 1) * size
    
    # 根据用户角色过滤数据
    filter_institution_id = institution_id
    if current_user.role == UserRole.OPERATOR:
        # 机构用户只能查看本机构的考生
        filter_institution_id = current_user.institution_id
    
    # 获取考生列表
    candidates = candidate_service.get_candidates(
        skip=skip,
        limit=size,
        institution_id=filter_institution_id,
        status=status
    )
    
    # 获取总数
    total = candidate_service.get_candidates_count(
        institution_id=filter_institution_id,
        status=status
    )
    
    # 转换为响应格式
    candidate_responses = []
    for candidate in candidates:
        candidate_responses.append(CandidateResponse(
            id=candidate.id,
            real_name=candidate.real_name,
            id_card=candidate.id_card,
            exam_product_id=candidate.exam_registrations[0].exam_product_id if candidate.exam_registrations else 0,
            institution_id=candidate.institution_id,
            phone=candidate.phone,
            email=candidate.email,
            username=candidate.username,
            role=candidate.role.value,
            is_active=candidate.is_active,
            is_verified=candidate.is_verified,
            created_at=candidate.created_at,
            updated_at=candidate.updated_at,
            last_login=candidate.last_login
        ))
    
    return CandidateList(
        items=candidate_responses,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{candidate_id}", response_model=CandidateResponse, summary="获取考生详情")
async def get_candidate(
    candidate_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """根据ID获取指定考生的详细信息"""
    candidate_service = CandidateService(db)
    candidate = candidate_service.get_candidate_by_id(candidate_id)
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在"
        )
    
    # 权限检查
    if current_user.role == UserRole.OPERATOR:
        if candidate.institution_id != current_user.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问该考生信息"
            )
    
    # 构建报名记录
    registrations = []
    for reg in candidate.exam_registrations:
        registrations.append({
            "id": reg.id,
            "exam_product_id": reg.exam_product_id,
            "registration_number": reg.registration_number,
            "status": reg.status.value,
            "created_at": reg.created_at.isoformat() if reg.created_at else None
        })
    
    return CandidateResponse(
        id=candidate.id,
        real_name=candidate.real_name,
        id_card=candidate.id_card,
        exam_product_id=candidate.exam_registrations[0].exam_product_id if candidate.exam_registrations else 0,
        institution_id=candidate.institution_id,
        phone=candidate.phone,
        email=candidate.email,
        username=candidate.username,
        role=candidate.role.value,
        is_active=candidate.is_active,
        is_verified=candidate.is_verified,
        created_at=candidate.created_at,
        updated_at=candidate.updated_at,
        last_login=candidate.last_login,
        registrations=registrations
    )


@router.post("/", response_model=CandidateResponse, summary="创建考生")
async def create_candidate(
    candidate_data: CandidateCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """创建新考生"""
    candidate_service = CandidateService(db)
    
    # 权限检查
    if current_user.role == UserRole.OPERATOR:
        if candidate_data.institution_id != current_user.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权为其他机构创建考生"
            )
    
    try:
        candidate = candidate_service.create_candidate(candidate_data)
        return CandidateResponse(
            id=candidate.id,
            real_name=candidate.real_name,
            id_card=candidate.id_card,
            exam_product_id=candidate_data.exam_product_id,
            institution_id=candidate.institution_id,
            phone=candidate.phone,
            email=candidate.email,
            username=candidate.username,
            role=candidate.role.value,
            is_active=candidate.is_active,
            is_verified=candidate.is_verified,
            created_at=candidate.created_at,
            updated_at=candidate.updated_at,
            last_login=candidate.last_login
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{candidate_id}", response_model=CandidateResponse, summary="更新考生")
async def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """更新指定考生的信息"""
    candidate_service = CandidateService(db)
    candidate = candidate_service.get_candidate_by_id(candidate_id)
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在"
        )
    
    # 权限检查
    if current_user.role == UserRole.OPERATOR:
        if candidate.institution_id != current_user.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改该考生信息"
            )
    
    try:
        updated_candidate = candidate_service.update_candidate(candidate_id, candidate_data)
        return CandidateResponse(
            id=updated_candidate.id,
            real_name=updated_candidate.real_name,
            id_card=updated_candidate.id_card,
            exam_product_id=updated_candidate.exam_registrations[0].exam_product_id if updated_candidate.exam_registrations else 0,
            institution_id=updated_candidate.institution_id,
            phone=updated_candidate.phone,
            email=updated_candidate.email,
            username=updated_candidate.username,
            role=updated_candidate.role.value,
            is_active=updated_candidate.is_active,
            is_verified=updated_candidate.is_verified,
            created_at=updated_candidate.created_at,
            updated_at=updated_candidate.updated_at,
            last_login=updated_candidate.last_login
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{candidate_id}", summary="删除考生")
async def delete_candidate(
    candidate_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """删除指定的考生（软删除）"""
    candidate_service = CandidateService(db)
    candidate = candidate_service.get_candidate_by_id(candidate_id)
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在"
        )
    
    # 权限检查
    if current_user.role == UserRole.OPERATOR:
        if candidate.institution_id != current_user.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除该考生"
            )
    elif current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    
    try:
        candidate_service.delete_candidate(candidate_id)
        return {"message": "考生删除成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除考生失败: {str(e)}"
        )


@router.post("/batch-import", response_model=BatchImportResult, summary="批量导入考生")
async def batch_import_candidates(
    file: UploadFile = File(...),
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """批量导入考生（Excel文件）"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持Excel文件格式"
        )
    
    try:
        # 读取Excel文件
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # 确定机构ID
        institution_id = None
        if current_user.role == UserRole.OPERATOR:
            institution_id = current_user.institution_id
        
        # 执行批量导入
        candidate_service = CandidateService(db)
        result = candidate_service.batch_import_candidates(df, institution_id)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量导入失败: {str(e)}"
        )


@router.get("/template/download", summary="下载考生导入模板")
async def download_candidate_template():
    """下载考生批量导入的Excel模板"""
    from fastapi.responses import FileResponse
    import tempfile
    import os
    
    # 创建模板数据
    template_data = {
        '姓名': ['张三', '李四'],
        '身份证号': ['110101199001011234', '110101199001011235'],
        '考试产品名称': ['无人机驾驶员', '无人机驾驶员'],
        '手机号（可选）': ['13800138000', '13800138001'],
        '邮箱（可选）': ['zhangsan@example.com', 'lisi@example.com']
    }
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        df = pd.DataFrame(template_data)
        df.to_excel(tmp_file.name, index=False)
        tmp_file_path = tmp_file.name
    
    return FileResponse(
        path=tmp_file_path,
        filename="考生导入模板.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.get("/statistics", response_model=CandidateStatistics, summary="获取考生统计信息")
async def get_candidate_statistics(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生统计信息"""
    candidate_service = CandidateService(db)
    
    # 根据用户角色确定统计范围
    institution_id = None
    if current_user.role == UserRole.OPERATOR:
        institution_id = current_user.institution_id
    
    stats = candidate_service.get_candidate_statistics(institution_id)
    return CandidateStatistics(**stats)