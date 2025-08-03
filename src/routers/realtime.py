"""
实时功能API路由
提供实时排队状态、公共看板等实时信息服务
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict, Any
from datetime import datetime, time
from pydantic import BaseModel

router = APIRouter(
    prefix="/realtime",
    tags=["realtime"],
)

# ===== 数据模型 =====

class QueueStatus(BaseModel):
    """排队状态"""
    venue_id: int
    venue_name: str
    current_position: int
    total_waiting: int
    estimated_wait_minutes: int
    current_activity: Optional[str] = None

class VenueStatus(BaseModel):
    """考场状态"""
    venue_id: int
    venue_name: str
    venue_type: str
    status: str  # active, maintenance, closed
    current_candidate: Optional[str] = None
    waiting_count: int
    next_start_time: Optional[str] = None

class PublicBoardData(BaseModel):
    """公共看板数据"""
    venues: List[VenueStatus]
    summary: Dict[str, Any]
    last_updated: str

# ===== 模拟实时数据 =====

def get_mock_venue_statuses():
    """获取模拟的考场状态数据"""
    return [
        {
            "venue_id": 1,
            "venue_name": "理论考场A",
            "venue_type": "理论考试",
            "status": "active",
            "current_candidate": "张*",
            "waiting_count": 8,
            "next_start_time": "09:15:00",
            "current_exam": "无人机驾驶员理论考试",
            "progress": "进行中 (还剩45分钟)"
        },
        {
            "venue_id": 2,
            "venue_name": "理论考场B", 
            "venue_type": "理论考试",
            "status": "active",
            "current_candidate": "李*",
            "waiting_count": 5,
            "next_start_time": "09:30:00",
            "current_exam": "航拍摄影师理论考试",
            "progress": "进行中 (还剩30分钟)"
        },
        {
            "venue_id": 3,
            "venue_name": "实操场地1",
            "venue_type": "实操考试", 
            "status": "active",
            "current_candidate": "王*",
            "waiting_count": 12,
            "next_start_time": "09:05:00",
            "current_exam": "多旋翼实操考试",
            "progress": "进行中 (还剩8分钟)"
        },
        {
            "venue_id": 4,
            "venue_name": "实操场地2",
            "venue_type": "实操考试",
            "status": "maintenance",
            "current_candidate": None,
            "waiting_count": 0,
            "next_start_time": None,
            "current_exam": "设备维护中",
            "progress": "预计10:00恢复"
        },
        {
            "venue_id": 5,
            "venue_name": "候考区A",
            "venue_type": "候考", 
            "status": "active",
            "current_candidate": None,
            "waiting_count": 15,
            "next_start_time": None,
            "current_exam": "考生等待中",
            "progress": "15人等待实操考试"
        }
    ]

def get_mock_queue_data():
    """获取模拟的排队数据"""
    return {
        1: {  # 张三
            "candidate_id": 1,
            "candidate_name": "张三",
            "queue_info": {
                "venue_id": 1,
                "venue_name": "理论考场A", 
                "position": 2,
                "total_waiting": 8,
                "estimated_wait_minutes": 25,
                "current_activity": "理论考试"
            }
        },
        2: {  # 李四
            "candidate_id": 2,
            "candidate_name": "李四",
            "queue_info": {
                "venue_id": 3,
                "venue_name": "实操场地1",
                "position": 5,
                "total_waiting": 12, 
                "estimated_wait_minutes": 65,
                "current_activity": "实操考试"
            }
        },
        3: {  # 王五
            "candidate_id": 3,
            "candidate_name": "王五",
            "queue_info": {
                "venue_id": 5,
                "venue_name": "候考区A",
                "position": 8,
                "total_waiting": 15,
                "estimated_wait_minutes": 120,
                "current_activity": "候考"
            }
        }
    }

# ===== 实时排队状态接口 =====

@router.get("/queue-status/{candidate_id}")
async def get_candidate_queue_status(candidate_id: int):
    """获取考生的实时排队状态"""
    
    queue_data = get_mock_queue_data()
    candidate_queue = queue_data.get(candidate_id)
    
    if not candidate_queue:
        # 考生可能没有在排队或已完成考试
        return {
            "message": "当前无排队信息",
            "candidate_id": candidate_id,
            "status": "no_queue",
            "possible_reasons": [
                "暂未安排考试",
                "考试已完成",
                "不在当前考试时段"
            ]
        }
    
    queue_info = candidate_queue["queue_info"]
    
    # 计算更详细的等待信息
    estimated_time = queue_info["estimated_wait_minutes"]
    hours = estimated_time // 60
    minutes = estimated_time % 60
    
    time_text = ""
    if hours > 0:
        time_text = f"{hours}小时{minutes}分钟"
    else:
        time_text = f"{minutes}分钟"
    
    return {
        "message": "排队状态获取成功",
        "candidate_id": candidate_id,
        "candidate_name": candidate_queue["candidate_name"],
        "queue_status": {
            "venue": queue_info["venue_name"],
            "activity": queue_info["current_activity"],
            "position": queue_info["position"],
            "total_waiting": queue_info["total_waiting"],
            "estimated_wait": time_text,
            "estimated_minutes": estimated_time,
            "status_text": f"您在{queue_info['venue_name']}排第{queue_info['position']}位",
            "advice": f"预计等待{time_text}，请耐心等候"
        },
        "last_updated": datetime.now().isoformat()
    }

@router.get("/venue-queue/{venue_id}")
async def get_venue_queue_status(venue_id: int):
    """获取指定考场的排队状态"""
    
    venues = get_mock_venue_statuses()
    venue = next((v for v in venues if v["venue_id"] == venue_id), None)
    
    if not venue:
        raise HTTPException(status_code=404, detail="考场不存在")
    
    # 模拟考场排队详情
    queue_details = []
    if venue["waiting_count"] > 0:
        for i in range(min(venue["waiting_count"], 10)):  # 只显示前10位
            queue_details.append({
                "position": i + 1,
                "candidate_name": f"考生{i+1}*",
                "exam_type": venue["current_exam"],
                "estimated_start": f"{9 + (i * 15) // 60:02d}:{(i * 15) % 60:02d}"
            })
    
    return {
        "message": f"{venue['venue_name']}排队状态",
        "venue_info": venue,
        "queue_details": queue_details,
        "summary": {
            "total_waiting": venue["waiting_count"],
            "current_status": venue["status"],
            "next_available": venue["next_start_time"]
        },
        "last_updated": datetime.now().isoformat()
    }

# ===== 公共看板接口 =====

@router.get("/public-board")
async def get_public_board():
    """获取公共看板实时数据"""
    
    venues = get_mock_venue_statuses()
    
    # 计算汇总信息
    active_venues = [v for v in venues if v["status"] == "active"]
    total_waiting = sum(v["waiting_count"] for v in venues)
    active_exams = len([v for v in active_venues if v["current_candidate"]])
    
    summary = {
        "total_venues": len(venues),
        "active_venues": len(active_venues), 
        "maintenance_venues": len([v for v in venues if v["status"] == "maintenance"]),
        "total_waiting_candidates": total_waiting,
        "active_exams": active_exams,
        "current_time": datetime.now().strftime("%H:%M:%S"),
        "last_refresh": datetime.now().isoformat()
    }
    
    return {
        "message": "公共看板数据获取成功",
        "venues": venues,
        "summary": summary,
        "last_updated": datetime.now().isoformat(),
        "refresh_interval": 10,  # 建议10秒刷新一次
        "announcements": [
            "考试期间请保持安静",
            "实操场地2设备维护中，预计10:00恢复",
            "理论考试请提前15分钟到达考场"
        ]
    }

@router.get("/public-board/venues-summary")
async def get_venues_summary():
    """获取考场简要状态（适合大屏显示）"""
    
    venues = get_mock_venue_statuses()
    
    # 简化的考场状态，适合大屏展示
    summary_venues = []
    for venue in venues:
        status_color = {
            "active": "green",
            "maintenance": "orange", 
            "closed": "red"
        }.get(venue["status"], "gray")
        
        summary_venues.append({
            "name": venue["venue_name"],
            "type": venue["venue_type"],
            "status": venue["status"],
            "status_color": status_color,
            "current": venue["current_candidate"] or "空闲",
            "waiting": venue["waiting_count"],
            "progress": venue["progress"]
        })
    
    return {
        "title": "考场实时状态",
        "venues": summary_venues,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_waiting": sum(v["waiting_count"] for v in venues),
        "display_mode": "large_screen"
    }

# ===== 系统状态接口 =====

@router.get("/venue-status")
async def get_venue_status():
    """获取所有考场的实时状态"""
    venues = get_mock_venue_statuses()
    return {
        "message": "考场状态获取成功",
        "venues": venues,
        "timestamp": datetime.now().isoformat(),
        "total_venues": len(venues)
    }

@router.get("/system-status")
async def get_system_status():
    """获取系统实时状态"""
    
    return {
        "message": "系统状态正常",
        "system_info": {
            "server_time": datetime.now().isoformat(),
            "uptime": "2小时15分钟",
            "active_connections": 45,
            "total_requests": 1247,
            "error_rate": "0.1%"
        },
        "exam_status": {
            "today_total_candidates": 89,
            "completed_exams": 34,
            "in_progress": 8,
            "waiting": 25,
            "scheduled": 22
        },
        "venue_summary": {
            "total_venues": 5,
            "active": 4,
            "maintenance": 1,
            "average_utilization": "78%"
        }
    }

@router.get("/notifications")
async def get_realtime_notifications(
    candidate_id: Optional[int] = Query(None, description="考生ID"),
    venue_id: Optional[int] = Query(None, description="考场ID")
):
    """获取实时通知"""
    
    # 模拟通知数据
    notifications = [
        {
            "id": 1,
            "type": "queue_update",
            "title": "排队状态更新",
            "message": "您的排队位置前进了2位",
            "timestamp": datetime.now().isoformat(),
            "priority": "normal",
            "target_candidate": 1
        },
        {
            "id": 2,
            "type": "venue_status",
            "title": "考场状态变更", 
            "message": "实操场地2设备维护完成，即将恢复使用",
            "timestamp": datetime.now().isoformat(),
            "priority": "high",
            "target_venue": 4
        },
        {
            "id": 3,
            "type": "general",
            "title": "系统公告",
            "message": "考试期间请保持安静，遵守考场纪律",
            "timestamp": datetime.now().isoformat(),
            "priority": "low"
        }
    ]
    
    # 过滤通知
    filtered_notifications = notifications
    if candidate_id:
        filtered_notifications = [n for n in notifications if 
                                n.get("target_candidate") == candidate_id or 
                                n["type"] == "general"]
    if venue_id:
        filtered_notifications = [n for n in notifications if 
                                n.get("target_venue") == venue_id or 
                                n["type"] == "general"]
    
    return {
        "message": "实时通知获取成功",
        "notifications": filtered_notifications,
        "unread_count": len(filtered_notifications),
        "last_updated": datetime.now().isoformat()
    }