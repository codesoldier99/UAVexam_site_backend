from fastapi import APIRouter, Query, Depends, HTTPException, Path, Body
from fastapi import status as http_status
from sqlalchemy.orm import Session
from typing import Optional, List
import logging
from src.dependencies.get_db import get_db
from src.dependencies.get_current_user import get_current_user
from src.models.user import User
from src.services.exam_product import ExamProductService
from src.schemas.exam_product import (
    ExamProductCreate, ExamProductUpdate, ExamProductRead, 
    ExamProductListResponse, ExamProductResponse, ExamProductQuery,
    ExamProductBatchUpdate, ExamProductStats, ExamProductStatsResponse,
    ExamCategory, ExamType, ExamClass, ExamLevel, ExamProductStatus
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/exam-products",
    tags=["考试产品管理"],
    responses={404: {"description": "未找到"}}
)

@router.post("/", 
    response_model=ExamProductResponse,
    status_code=http_status.HTTP_201_CREATED,
    summary="创建考试产品",
    description="创建新的考试产品，需要管理员权限"
)
async def create_exam_product(
    exam_product: ExamProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建考试产品"""
    try:
        # 调用服务层创建产品
        db_exam_product = ExamProductService.create(
            db=db, 
            exam_product=exam_product,
            user_id=current_user.id
        )
        
        return ExamProductResponse(
            success=True,
            message="考试产品创建成功",
            data=db_exam_product
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"创建考试产品失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建考试产品失败"
        )



@router.get("/",
    response_model=ExamProductListResponse,
    summary="获取考试产品列表",
    description="获取考试产品列表，支持分页、搜索和筛选"
)
async def get_exam_products(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    category: Optional[ExamCategory] = Query(None, description="考试类别筛选"),
    exam_type: Optional[ExamType] = Query(None, description="考试类型筛选"),
    exam_class: Optional[ExamClass] = Query(None, description="考试等级筛选"),
    exam_level: Optional[ExamLevel] = Query(None, description="考试级别筛选"),
    status: Optional[ExamProductStatus] = Query(None, description="状态筛选"),
    min_price: Optional[float] = Query(None, ge=0, description="最低价格"),
    max_price: Optional[float] = Query(None, ge=0, description="最高价格"),
    sort_by: Optional[str] = Query("created_at", description="排序字段"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取考试产品列表"""
    try:
        # 直接构建过滤条件字典 - 产业级实现
        filters = {}
        
        if search:
            filters['search'] = search
        if category:
            filters['category'] = category
        if exam_type:
            filters['exam_type'] = exam_type
        if exam_class:
            filters['exam_class'] = exam_class
        if exam_level:
            filters['exam_level'] = exam_level
        if status:
            filters['status'] = status
        if min_price is not None:
            filters['min_price'] = min_price
        if max_price is not None:
            filters['max_price'] = max_price
        if sort_by:
            filters['sort_by'] = sort_by
        if sort_order:
            filters['sort_order'] = sort_order
        
        # 调用服务层获取数据
        products, total = ExamProductService.get_multi(
            db=db,
            page=page,
            size=size,
            filters=filters
        )
        
        # 计算分页信息
        total_pages = (total + size - 1) // size
        
        # 产业级数据序列化，处理脏数据
        serialized_products = [ExamProductRead.from_orm(product) for product in products]
        
        return ExamProductListResponse(
            success=True,
            message="获取考试产品列表成功",
            data=serialized_products,
            pagination={
                "page": page,
                "size": size,
                "total": total,
                "pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            },
            filters=filters
        )
        
    except Exception as e:
        logger.error(f"获取考试产品列表失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考试产品列表失败"
        )

@router.get("/{product_id}",
    response_model=ExamProductResponse,
    summary="获取考试产品详情",
    description="根据ID获取指定考试产品的详细信息"
)
async def get_exam_product(
    product_id: int = Path(..., description="考试产品ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取考试产品详情"""
    try:
        db_exam_product = ExamProductService.get(db, product_id)
        
        if not db_exam_product:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"未找到ID为 {product_id} 的考试产品"
            )
        
        return ExamProductResponse(
            success=True,
            message="获取考试产品详情成功",
            data=db_exam_product
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取考试产品详情失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考试产品详情失败"
        )

@router.put("/{product_id}",
    response_model=ExamProductResponse,
    summary="更新考试产品",
    description="更新指定ID的考试产品信息"
)
async def update_exam_product(
    product_id: int = Path(..., description="考试产品ID"),
    exam_product: ExamProductUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新考试产品"""
    try:
        # 检查产品是否存在
        existing_product = ExamProductService.get(db, product_id)
        if not existing_product:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"未找到ID为 {product_id} 的考试产品"
            )
        
        # 更新产品
        updated_product = ExamProductService.update(
            db=db,
            product_id=product_id,
            exam_product=exam_product,
            user_id=current_user.id
        )
        
        return ExamProductResponse(
            success=True,
            message="考试产品更新成功",
            data=updated_product
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新考试产品失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新考试产品失败"
        )

@router.delete("/{product_id}",
    summary="删除考试产品",
    description="删除指定ID的考试产品（软删除）"
)
async def delete_exam_product(
    product_id: int = Path(..., description="考试产品ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除考试产品（软删除）"""
    try:
        success = ExamProductService.delete(
            db=db,
            product_id=product_id,
            user_id=current_user.id
        )
        
        if not success:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"未找到ID为 {product_id} 的考试产品"
            )
        
        return {
            "success": True,
            "message": "考试产品删除成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除考试产品失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除考试产品失败"
        )

@router.patch("/batch/status",
    summary="批量更新考试产品状态",
    description="批量更新多个考试产品的状态或激活状态"
)
async def batch_update_exam_products(
    batch_update: ExamProductBatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量更新考试产品状态"""
    try:
        result = ExamProductService.batch_update_status(
            db=db,
            batch_update=batch_update,
            user_id=current_user.id
        )
        
        return {
            "success": result["success"],
            "message": f"批量更新完成，成功更新 {result['updated_count']}/{result['total_count']} 个产品",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"批量更新考试产品失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="批量更新考试产品失败"
        )

@router.get("/stats/overview",
    response_model=ExamProductStatsResponse,
    summary="获取考试产品统计信息",
    description="获取考试产品的各种统计数据"
)
async def get_exam_product_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取考试产品统计信息"""
    try:
        stats = ExamProductService.get_statistics(db)
        
        return ExamProductStatsResponse(
            success=True,
            message="获取统计信息成功",
            data=ExamProductStats(**stats)
        )
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取统计信息失败"
        )

@router.get("/active/list",
    response_model=List[ExamProductRead],
    summary="获取激活的考试产品",
    description="获取所有激活状态的考试产品列表"
)
async def get_active_exam_products(
    limit: int = Query(50, ge=1, le=100, description="返回数量限制"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取激活的考试产品"""
    try:
        products = ExamProductService.get_active_products(db, limit)
        
        return products
        
    except Exception as e:
        logger.error(f"获取激活产品失败: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取激活产品失败"
        )