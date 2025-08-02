from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.dependencies.get_db import get_db
from src.auth.fastapi_users_config import current_active_user
from src.models.user import User
from src.models.candidate import Candidate
from src.institutions.models import Institution
from src.models.exam_product import ExamProduct
from src.schemas.candidate import (
    CandidateCreate, CandidateRead, CandidateUpdate, 
    CandidateListResponse, BatchImportResponse
)
import pandas as pd
import io
from io import BytesIO

router = APIRouter(prefix="/candidates", tags=["考生管理"])

@router.post("/", response_model=CandidateRead, status_code=201)
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """手动添加考生"""
    # 权限检查：机构用户
    if not current_user.institution_id:
        raise HTTPException(status_code=403, detail="只有机构用户可以添加考生")
    
    # 检查身份证号是否已存在
    existing_candidate = db.query(Candidate).filter(Candidate.id_card == candidate.id_card).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail="身份证号已存在")
    
    # 检查机构是否存在
    institution = db.query(Institution).filter(Institution.id == candidate.institution_id).first()
    if not institution:
        raise HTTPException(status_code=400, detail="机构不存在")
    
    # 检查考试产品是否存在
    exam_product = db.query(ExamProduct).filter(ExamProduct.id == candidate.exam_product_id).first()
    if not exam_product:
        raise HTTPException(status_code=400, detail="考试产品不存在")
    
    # 设置机构ID为当前用户的机构
    candidate.institution_id = current_user.institution_id
    
    # 创建新考生
    new_candidate = Candidate(
        name=candidate.name,
        id_card=candidate.id_card,
        institution_id=candidate.institution_id,
        exam_product_id=candidate.exam_product_id,
        status=candidate.status
    )
    
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    
    return new_candidate

@router.post("/batch", response_model=BatchImportResponse)
def batch_import_candidates(
    institution_id: int,
    exam_product_id: int,
    candidates: List[dict],
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """批量导入考生"""
    # 权限检查：机构用户
    if not current_user.institution_id:
        raise HTTPException(status_code=403, detail="只有机构用户可以批量导入考生")
    
    # 检查机构是否存在
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(status_code=400, detail="机构不存在")
    
    # 检查考试产品是否存在
    exam_product = db.query(ExamProduct).filter(ExamProduct.id == exam_product_id).first()
    if not exam_product:
        raise HTTPException(status_code=400, detail="考试产品不存在")
    
    success_count = 0
    failed_count = 0
    failed_items = []
    
    for candidate_data in candidates:
        try:
            # 检查身份证号是否已存在
            existing = db.query(Candidate).filter(Candidate.id_card == candidate_data["id_card"]).first()
            if existing:
                failed_count += 1
                failed_items.append(f"身份证号 {candidate_data['id_card']} 已存在")
                continue
            
            # 创建新考生
            new_candidate = Candidate(
                name=candidate_data["name"],
                id_card=candidate_data["id_card"],
                institution_id=institution_id,
                exam_product_id=exam_product_id,
                status="待排期"
            )
            
            db.add(new_candidate)
            success_count += 1
            
        except Exception as e:
            failed_count += 1
            failed_items.append(f"考生 {candidate_data.get('name', '未知')}: {str(e)}")
    
    db.commit()
    
    return BatchImportResponse(
        success_count=success_count,
        failed_count=failed_count,
        errors=failed_items
    )

@router.get("/batch-import/template")
def download_import_template():
    """下载导入模板"""
    # 创建简单的Excel模板
    import pandas as pd
    
    # 创建模板数据
    template_data = pd.DataFrame({
        'name': ['张三', '李四'],
        'id_card': ['110101199001011234', '110101199001011235'],
        'phone': ['13800138001', '13800138002']
    })
    
    # 保存到BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        template_data.to_excel(writer, index=False, sheet_name='考生信息')
    
    output.seek(0)
    
    return StreamingResponse(
        BytesIO(output.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=candidates_template.xlsx"}
    )

@router.post("/batch-import")
def batch_import_candidates_file(
    file: UploadFile = File(...),
    institution_id: int = Query(...),
    exam_product_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """通过文件批量导入考生"""
    # 权限检查：机构用户
    if not current_user.institution_id:
        raise HTTPException(status_code=403, detail="只有机构用户可以批量导入考生")
    
    # 检查文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持Excel文件格式")
    
    try:
        # 读取Excel文件
        content = file.file.read()
        df = pd.read_excel(io.BytesIO(content))
        
        success_count = 0
        failed_count = 0
        failed_items = []
        
        for _, row in df.iterrows():
            try:
                # 检查身份证号是否已存在
                existing = db.query(Candidate).filter(Candidate.id_card == row['id_card']).first()
                if existing:
                    failed_count += 1
                    failed_items.append(f"身份证号 {row['id_card']} 已存在")
                    continue
                
                # 创建新考生
                new_candidate = Candidate(
                    name=row['name'],
                    id_card=row['id_card'],
                    institution_id=institution_id,
                    exam_product_id=exam_product_id,
                    status="待排期"
                )
                
                db.add(new_candidate)
                success_count += 1
                
            except Exception as e:
                failed_count += 1
                failed_items.append(f"行 {_ + 2}: {str(e)}")
        
        db.commit()
        
        return {
            "message": f"导入完成：成功 {success_count} 条，失败 {failed_count} 条",
            "success_count": success_count,
            "failed_count": failed_count,
            "failed_items": failed_items
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"文件处理失败：{str(e)}")

@router.get("/", response_model=List[CandidateRead])
def get_candidates(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    institution_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """查询考生列表"""
    # 权限检查：考务管理员或机构用户
    if not current_user.institution_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 机构用户只能查询本机构考生
    if current_user.institution_id:
        institution_id = current_user.institution_id
    
    query = db.query(Candidate)
    
    # 机构过滤
    if institution_id:
        query = query.filter(Candidate.institution_id == institution_id)
    
    # 状态过滤
    if status:
        query = query.filter(Candidate.status == status)
    
    # 搜索过滤
    if search:
        query = query.filter(
            (Candidate.name.contains(search)) | 
            (Candidate.id_card.contains(search))
        )
    
    skip = (page - 1) * size
    candidates = query.offset(skip).limit(size).all()
    
    return candidates

@router.get("/{candidate_id}", response_model=CandidateRead)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """获取考生详情"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="考生不存在")
    
    # 权限检查：机构用户只能查看本机构考生
    if current_user.institution_id and candidate.institution_id != current_user.institution_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return candidate

@router.put("/{candidate_id}", response_model=CandidateRead)
def update_candidate(
    candidate_id: int,
    candidate: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """更新考生信息"""
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="考生不存在")
    
    # 权限检查：机构用户只能更新本机构考生
    if current_user.institution_id and db_candidate.institution_id != current_user.institution_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 更新字段
    update_data = candidate.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_candidate, field, value)
    
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.delete("/{candidate_id}", status_code=204)
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """删除考生"""
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="考生不存在")
    
    # 权限检查：机构用户只能删除本机构考生
    if current_user.institution_id and db_candidate.institution_id != current_user.institution_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    db.delete(db_candidate)
    db.commit()
    
    return {"message": "考生删除成功"} 