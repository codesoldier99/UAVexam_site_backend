from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date, time

class ScheduleBase(BaseModel):
    scheduled_date: datetime
    start_time: datetime
    end_time: datetime
    candidate_id: int
    exam_product_id: int
    venue_id: Optional[int] = None
    schedule_type: str
    status: Optional[str] = "pending"
    check_in_status: Optional[str] = "not_checked_in"
    notes: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleRead(ScheduleBase):
    id: int
    check_in_time: Optional[datetime] = None
    queue_position: Optional[int] = None
    estimated_wait_time: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    # 关联信息
    candidate_name: Optional[str] = None
    venue_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ScheduleUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    candidate_id: Optional[int] = None
    exam_product_id: Optional[int] = None
    venue_id: Optional[int] = None
    schedule_type: Optional[str] = None
    status: Optional[str] = None
    check_in_status: Optional[str] = None
    notes: Optional[str] = None

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