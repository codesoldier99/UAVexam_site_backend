from fastapi import APIRouter, Query, Depends
from typing import Optional
from src.core.rbac import require_permission, Permission
from src.db.models import User

router = APIRouter(
    prefix="/exam-products",
    tags=["exam_products"],
)

@router.get("/")
async def get_exam_products(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    category: Optional[str] = Query(None, description="考试类别筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    difficulty: Optional[str] = Query(None, description="难度筛选"),
    current_user: User = Depends(require_permission(Permission.EXAM_PRODUCT_MANAGE))
):
    """获取考试产品列表 - 增强版本支持分页和筛选"""
    
    # 模拟考试产品数据
    all_exam_products = [
        {"id": 1, "name": "无人机驾驶员考试", "description": "民用无人机驾驶员资格考试", "category": "理论+实操", "duration": 120, "status": "active", "difficulty": "中等", "price": 500.0},
        {"id": 2, "name": "航拍摄影师认证", "description": "专业航拍摄影师技能认证", "category": "实操", "duration": 90, "status": "active", "difficulty": "简单", "price": 300.0},
        {"id": 3, "name": "无人机维修技师", "description": "无人机维修保养技师考试", "category": "理论", "duration": 150, "status": "active", "difficulty": "困难", "price": 800.0},
        {"id": 4, "name": "无人机教练员", "description": "无人机培训教练员资格考试", "category": "理论+实操", "duration": 180, "status": "inactive", "difficulty": "困难", "price": 1000.0},
        {"id": 5, "name": "农业植保飞行", "description": "农业植保无人机操作考试", "category": "实操", "duration": 100, "status": "active", "difficulty": "中等", "price": 600.0},
        {"id": 6, "name": "消防救援飞行", "description": "消防救援无人机操作考试", "category": "理论+实操", "duration": 160, "status": "active", "difficulty": "困难", "price": 1200.0}
    ]
    
    # 根据参数筛选数据
    filtered_products = all_exam_products
    if category:
        filtered_products = [p for p in filtered_products if p["category"] == category]
    if status:
        filtered_products = [p for p in filtered_products if p["status"] == status]
    if difficulty:
        filtered_products = [p for p in filtered_products if p["difficulty"] == difficulty]
    
    # 分页处理
    total = len(filtered_products)
    start = (page - 1) * size
    end = start + size
    products_page = filtered_products[start:end]
    
    return {
        "message": "考试产品列表接口 - 支持分页和筛选",
        "data": products_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "filters": {
            "category": category,
            "status": status,
            "difficulty": difficulty
        }
    }

@router.get("/{product_id}")
async def get_exam_product_by_id(product_id: int):
    """根据ID获取单个考试产品信息"""
    products = {
        1: {"id": 1, "name": "无人机驾驶员考试", "description": "民用无人机驾驶员资格考试", "category": "理论+实操", "duration": 120, "status": "active"},
        2: {"id": 2, "name": "航拍摄影师认证", "description": "专业航拍摄影师技能认证", "category": "实操", "duration": 90, "status": "active"},
        3: {"id": 3, "name": "无人机维修技师", "description": "无人机维修保养技师考试", "category": "理论", "duration": 150, "status": "active"}
    }
    
    if product_id not in products:
        return {"error": "考试产品不存在", "product_id": product_id}
    
    return {
        "message": "考试产品详情",
        "data": products[product_id]
    }
