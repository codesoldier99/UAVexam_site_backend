from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date, time

class ScheduleBase(BaseModel):
    exam_date: date
    start_time: time
    end_time: time
    candidate_id: int
    venue_id: int
    activity_name: str
    status: str = "待签到"

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleRead(ScheduleBase):
    id: int
    check_in_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # 关联信息
    candidate_name: Optional[str] = None
    venue_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ScheduleUpdate(BaseModel):
    exam_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    candidate_id: Optional[int] = None
    venue_id: Optional[int] = None
    activity_name: Optional[str] = None
    status: Optional[str] = None

class ScheduleListResponse(BaseModel):
    items: List[ScheduleRead]
    total: int
    page: int
    size: int
    pages: int

class BatchCreateScheduleRequest(BaseModel):
    schedules: List[ScheduleCreate]

class CheckInRequest(BaseModel):
    check_in_time: Optional[datetime] = None

class QueuePositionResponse(BaseModel):
    schedule_id: int
    position: int
    total_in_queue: int
    estimated_wait_time: Optional[int] = None  # 预计等待时间（分钟）
    status: str  # 排队状态：waiting, in_progress, completed 