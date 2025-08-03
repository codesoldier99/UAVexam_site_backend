from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/public", tags=["public"])

@router.get("/institutions")
async def get_institutions():
    """获取机构列表 - 公共API"""
    return [
        {
            "id": 1,
            "name": "示例培训机构",
            "contact_person": "张三",
            "phone": "13800138000"
        }
    ]

@router.get("/venues-status")
async def get_venues_status():
    """获取考场状态 - 公共API"""
    return [
        {
            "id": 1,
            "name": "北京考场1",
            "type": "理论考场",
            "status": "active"
        }
    ]

@router.get("/exam-products")
async def get_exam_products():
    """获取考试产品列表 - 公共API"""
    return [
        {
            "id": 1,
            "name": "无人机驾驶员考试",
            "description": "民用无人机驾驶员资格考试"
        }
    ]

@router.get("/health")
async def health_check():
    """健康检查 - 公共API"""
    return {
        "status": "healthy", 
        "message": "系统运行正常",
        "timestamp": datetime.now().isoformat()
    }
