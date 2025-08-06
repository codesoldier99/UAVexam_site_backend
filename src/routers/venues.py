from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy.orm import Session
from typing import Optional, List
from src.dependencies.get_db import get_db
from src.dependencies.get_current_user import get_current_user
from src.dependencies.permissions import (
    require_venue_view, require_venue_create, require_venue_update,
    require_venue_delete, require_venue_manage, require_venue_stats
)
from src.core.audit import (
    audit_venue_create, audit_venue_update, audit_venue_delete, audit_venue_read
)
from src.models.user import User
from src.services.venue import VenueService
from src.schemas.venue import (
    VenueCreate, VenueRead, VenueUpdate, VenueListResponse,
    VenueResponse, VenueListResponseWrapper, VenueBatchStatusUpdate
)

router = APIRouter(
    prefix="/venues",
    tags=["场地管理"],
)

@router.post("/", response_model=VenueResponse, status_code=http_status.HTTP_201_CREATED)
@audit_venue_create()
async def create_venue(
    venue: VenueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_venue_create())
):
    """创建新考场"""
    try:
        db_venue = await VenueService.create(db=db, venue=venue)
        return VenueResponse(
            code=201,
            message="考场创建成功",
            data=VenueRead.model_validate(db_venue)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"创建考场失败: {str(e)}"
        )

@router.get("/", response_model=VenueListResponseWrapper)
@audit_venue_read()
async def get_venues(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    status: Optional[str] = Query(None, description="状态筛选(active/inactive)"),
    venue_type: Optional[str] = Query(None, description="考场类型筛选"),
    search: Optional[str] = Query(None, description="搜索关键词(名称/地址/联系人)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_venue_view())
):
    """获取考场列表 - 支持分页、筛选和搜索"""
    try:
        skip = (page - 1) * size
        venues, total = await VenueService.get_multi(
            db=db, 
            skip=skip, 
            limit=size,
            status=status,
            venue_type=venue_type,
            search=search
        )
        
        venue_reads = [VenueRead.model_validate(venue) for venue in venues]
        pages = (total + size - 1) // size
        
        return VenueListResponseWrapper(
            code=200,
            message="获取考场列表成功",
            data=VenueListResponse(
                items=venue_reads,
                total=total,
                page=page,
                size=size,
                pages=pages
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取考场列表失败: {str(e)}"
        )

@router.get("/{venue_id}", response_model=VenueResponse)
@audit_venue_read()
async def get_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_venue_view())
):
    """根据ID获取考场详情"""
    db_venue = await VenueService.get(db=db, venue_id=venue_id)
    if not db_venue:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"考场不存在 (ID: {venue_id})"
        )
    
    return VenueResponse(
        code=200,
        message="获取考场详情成功",
        data=VenueRead.model_validate(db_venue)
    )

@router.put("/{venue_id}", response_model=VenueResponse)
@audit_venue_update()
async def update_venue(
    venue_id: int,
    venue: VenueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_venue_update())
):
    """更新考场信息"""
    db_venue = await VenueService.update(db=db, venue_id=venue_id, venue=venue)
    if not db_venue:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"考场不存在 (ID: {venue_id})"
        )
    
    return VenueResponse(
        code=200,
        message="考场更新成功",
        data=VenueRead.model_validate(db_venue)
    )

@router.delete("/{venue_id}")
@audit_venue_delete()
async def delete_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_venue_delete())
):
    """删除考场"""
    success = await VenueService.delete(db=db, venue_id=venue_id)
    if not success:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"考场不存在 (ID: {venue_id})"
        )
    
    return {
        "code": 200,
        "message": "考场删除成功",
        "data": {"deleted_id": venue_id}
    }

@router.get("/stats/overview")
async def get_venue_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_venue_stats())
):
    """获取考场统计信息"""
    try:
        stats = await VenueService.get_venue_stats(db=db)
        return {
            "code": 200,
            "message": "获取考场统计成功",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计信息失败: {str(e)}"
        )

@router.patch("/batch/status")
async def batch_update_status(
    batch_update: VenueBatchStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_venue_manage())
):
    """批量更新考场状态"""
    try:
        updated_count = await VenueService.bulk_update_status(
            db=db, 
            venue_ids=batch_update.venue_ids, 
            status=batch_update.new_status.value
        )
        return {
            "code": 200,
            "message": f"批量更新成功，共更新 {updated_count} 个考场",
            "data": {
                "updated_count": updated_count,
                "venue_ids": batch_update.venue_ids,
                "new_status": batch_update.new_status.value
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量更新失败: {str(e)}"
        )
