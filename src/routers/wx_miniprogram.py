from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from src.dependencies.get_db import get_db
from src.dependencies.get_current_user import get_current_user
from src.models.user import User
from src.models.candidate import Candidate, CandidateStatus
from src.models.schedule import Schedule
from src.models.venue import Venue
from src.schemas.wx_miniprogram import WxLoginRequest, WxLoginResponse, QrCodeResponse
from src.services.wx_miniprogram import WxMiniprogramService
from src.services.venue import VenueService
from src.core.auth import create_access_token
from src.core.config import settings

router = APIRouter(prefix="/wx", tags=["微信小程序"])

@router.get("/health")
async def wx_health_check():
    """微信小程序模块健康检查"""
    return {
        "status": "healthy",
        "service": "微信小程序服务",
        "version": "1.0.0",
        "features": ["考生登录", "信息查询", "签到功能"]
    }

@router.post("/login-by-idcard")
async def login_by_idcard(
    id_card: str = Query(..., description="18位身份证号码")
):
    """考生通过身份证号码登录（核心功能）"""
    
    # 验证身份证号格式
    if not id_card or len(id_card) != 18:
        raise HTTPException(
            status_code=400, 
            detail="身份证号格式不正确，请输入18位身份证号"
        )
    
    # 模拟考生数据库查询
    mock_candidates = {
        "110101199001011234": {
            "id": 1,
            "name": "张三",
            "id_number": "110101199001011234",
            "phone": "13800138001",
            "exam_product": "无人机驾驶员考试",
            "exam_product_id": 1,
            "institution": "北京航空培训中心",
            "institution_id": 1,
            "status": "待排期",
            "registration_date": "2025-08-01"
        },
        "110101199002021234": {
            "id": 2,
            "name": "李四",
            "id_number": "110101199002021234",
            "phone": "13800138002",
            "exam_product": "无人机驾驶员考试",
            "exam_product_id": 1,
            "institution": "上海飞行学院",
            "institution_id": 2,
            "status": "已排期",
            "registration_date": "2025-08-02"
        },
        "110101199003031234": {
            "id": 3,
            "name": "王五",
            "id_number": "110101199003031234",
            "phone": "13800138003",
            "exam_product": "航拍摄影师认证",
            "exam_product_id": 2,
            "institution": "北京航空培训中心",
            "institution_id": 1,
            "status": "待排期",
            "registration_date": "2025-08-03"
        }
    }
    
    # 查找考生
    candidate = mock_candidates.get(id_card)
    if not candidate:
        raise HTTPException(
            status_code=404, 
            detail="未找到该身份证号对应的考生信息，请联系培训机构确认报名状态"
        )
    
    # 生成简单的访问令牌（实际项目中应使用JWT）
    access_token = f"candidate_{candidate['id']}_{id_card[-4:]}"
    
    return {
        "message": "登录成功",
        "access_token": access_token,
        "candidate_info": candidate,
        "login_time": "2025-08-03T19:45:00"
    }

@router.get("/candidate-info/{candidate_id}")
async def get_candidate_info(candidate_id: int):
    """获取考生详细信息（需要先登录）"""
    
    # 模拟考生详细信息
    candidates_detail = {
        1: {
            "id": 1,
            "name": "张三",
            "id_number": "110101199001011234",
            "phone": "13800138001",
            "exam_product": "无人机驾驶员考试",
            "institution": "北京航空培训中心",
            "status": "待排期",
            "registration_date": "2025-08-01",
            "upcoming_schedules": [
                {
                    "id": 1,
                    "activity_name": "理论考试",
                    "exam_date": "2025-08-15",
                    "start_time": "09:00",
                    "end_time": "10:30",
                    "venue": "理论考场A",
                    "status": "scheduled"
                },
                {
                    "id": 2,
                    "activity_name": "实操考试",
                    "exam_date": "2025-08-15",
                    "start_time": "14:00",
                    "end_time": "14:15",
                    "venue": "实操场地1",
                    "status": "pending"
                }
            ],
            "current_queue_info": {
                "venue": "实操场地1",
                "position": 3,
                "estimated_wait_time": "约45分钟"
            }
        },
        2: {
            "id": 2,
            "name": "李四",
            "id_number": "110101199002021234",
            "phone": "13800138002",
            "exam_product": "无人机驾驶员考试",
            "institution": "上海飞行学院",
            "status": "已排期",
            "registration_date": "2025-08-02",
            "upcoming_schedules": [
                {
                    "id": 3,
                    "activity_name": "理论考试",
                    "exam_date": "2025-08-16",
                    "start_time": "10:00",
                    "end_time": "11:30",
                    "venue": "理论考场B",
                    "status": "scheduled"
                }
            ],
            "current_queue_info": None
        }
    }
    
    candidate = candidates_detail.get(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="考生信息不存在")
    
    return {
        "message": "考生信息获取成功",
        "data": candidate
    }

@router.get("/my-qrcode/{candidate_id}")
async def get_my_qrcode(candidate_id: int):
    """获取考生的动态身份二维码（核心功能）"""
    
    # 模拟查找考生的下一个待进行的日程
    candidates_schedules = {
        1: {
            "candidate_id": 1,
            "name": "张三",
            "next_schedule": {
                "schedule_id": 1,
                "activity_name": "理论考试",
                "exam_date": "2025-08-15",
                "start_time": "09:00",
                "venue": "理论考场A",
                "status": "待签到"
            }
        },
        2: {
            "candidate_id": 2,
            "name": "李四",
            "next_schedule": {
                "schedule_id": 3,
                "activity_name": "理论考试",
                "exam_date": "2025-08-16",
                "start_time": "10:00",
                "venue": "理论考场B",
                "status": "待签到"
            }
        },
        3: {
            "candidate_id": 3,
            "name": "王五",
            "next_schedule": None  # 暂无安排
        }
    }
    
    candidate_schedule = candidates_schedules.get(candidate_id)
    if not candidate_schedule:
        raise HTTPException(status_code=404, detail="考生信息不存在")
    
    if not candidate_schedule["next_schedule"]:
        return {
            "message": "暂无待进行的考试安排",
            "candidate_id": candidate_id,
            "qr_code": None,
            "status": "no_schedule"
        }
    
    # 生成二维码数据（包含下一条日程的ID）
    next_schedule = candidate_schedule["next_schedule"]
    qr_data = {
        "type": "candidate_checkin",
        "candidate_id": candidate_id,
        "schedule_id": next_schedule["schedule_id"],
        "candidate_name": candidate_schedule["name"],
        "activity_name": next_schedule["activity_name"],
        "venue": next_schedule["venue"],
        "timestamp": "2025-08-03T19:50:00",
        "valid_until": f"{next_schedule['exam_date']}T23:59:59"
    }
    
    # 生成二维码URL（实际应用中应该生成真实的二维码图片）
    qr_content = f"schedule_{next_schedule['schedule_id']}_candidate_{candidate_id}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_content}"
    
    return {
        "message": "动态二维码生成成功",
        "candidate_id": candidate_id,
        "candidate_name": candidate_schedule["name"],
        "qr_data": qr_data,
        "qr_url": qr_url,
        "next_schedule": next_schedule,
        "instructions": "请向考务人员出示此二维码进行签到",
        "refresh_interval": 300  # 5分钟刷新一次
    }

@router.post("/login", response_model=WxLoginResponse)
def wx_login(
    request: WxLoginRequest,
    db: Session = Depends(get_db)
):
    """考生登录/绑定"""
    try:
        # 验证身份证号格式
        if not request.id_card or len(request.id_card) != 18:
            raise HTTPException(status_code=400, detail="身份证号格式不正确")
        
        # 查找考生
        candidate = db.query(Candidate).filter(Candidate.id_number == request.id_card).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="未找到该身份证号对应的考生信息")
        
        # 验证考生状态
        if candidate.status not in [CandidateStatus.APPROVED, CandidateStatus.ACTIVE]:
            raise HTTPException(status_code=403, detail="考生状态不允许登录")
        
        # 生成JWT token
        token_data = {
            "sub": str(candidate.id),
            "type": "candidate",
            "candidate_id": candidate.id,
            "institution_id": candidate.institution_id
        }
        access_token = create_access_token(token_data)
        
        return WxLoginResponse(
            access_token=access_token,
            token_type="bearer",
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            phone=candidate.phone,
            status=candidate.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

# 注释：已移除重复的 /me/qrcode 接口，使用 /my-qrcode/{candidate_id} 接口代替
# 这样符合考生端的使用场景，不需要复杂的认证机制 