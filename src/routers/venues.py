from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(
    prefix="/venues",
    tags=["venues"],
)

@router.get("/")
async def get_venues(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    status: Optional[str] = Query(None, description="状态筛选"),
    venue_type: Optional[str] = Query(None, description="考场类型筛选")
):
    """获取场地列表 - 增强版本支持分页和筛选"""
    
    # 模拟数据库中的所有场地数据
    all_venues = [
        {"id": 1, "name": "北京考场1", "type": "理论考场", "address": "北京市朝阳区", "capacity": 50, "status": "active"},
        {"id": 2, "name": "北京考场2", "type": "实操考场", "address": "北京市海淀区", "capacity": 30, "status": "active"},
        {"id": 3, "name": "上海考场1", "type": "理论考场", "address": "上海市浦东新区", "capacity": 60, "status": "inactive"},
        {"id": 4, "name": "深圳考场1", "type": "理论考场", "address": "深圳市南山区", "capacity": 40, "status": "active"},
        {"id": 5, "name": "广州考场1", "type": "实操考场", "address": "广州市天河区", "capacity": 35, "status": "active"}
    ]
    
    # 根据参数筛选数据
    filtered_venues = all_venues
    if status:
        filtered_venues = [v for v in filtered_venues if v["status"] == status]
    if venue_type:
        filtered_venues = [v for v in filtered_venues if v["type"] == venue_type]
    
    # 分页处理
    total = len(filtered_venues)
    start = (page - 1) * size
    end = start + size
    venues_page = filtered_venues[start:end]
    
    return {
        "message": "场地列表接口 - 支持分页和筛选",
        "data": venues_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "filters": {
            "status": status,
            "venue_type": venue_type
        }
    }

@router.get("/{venue_id}")
async def get_venue_by_id(venue_id: int):
    """根据ID获取单个场地信息"""
    venues = {
        1: {"id": 1, "name": "北京考场1", "type": "理论考场", "address": "北京市朝阳区", "capacity": 50, "status": "active"},
        2: {"id": 2, "name": "北京考场2", "type": "实操考场", "address": "北京市海淀区", "capacity": 30, "status": "active"}
    }
    
    if venue_id not in venues:
        return {"error": "场地不存在", "venue_id": venue_id}
    
    return {
        "message": "场地详情",
        "data": venues[venue_id]
    }
