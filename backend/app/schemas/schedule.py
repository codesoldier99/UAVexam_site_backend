from typing import Optional, List
from pydantic import BaseModel
from datetime import date, time, datetime
from app.models.schedule import ScheduleStatus, ActivityType

class ScheduleBase(BaseModel):
    candidate_id: int
    venue_id: int
    exam_date: date
    start_time: time
    end_time: time
    activity_type: ActivityType
    activity_name: Optional[str] = None
    notes: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleBatchCreate(BaseModel):
    candidate_ids: List[int]
    venue_id: int
    exam_date: date
    start_time: time
    activity_type: ActivityType
    activity_name: Optional[str] = None
    duration_minutes: int = 15  # 每个考生的时长
    
class ScheduleUpdate(BaseModel):
    venue_id: Optional[int] = None
    exam_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[ScheduleStatus] = None
    notes: Optional[str] = None

class Schedule(ScheduleBase):
    id: int
    status: ScheduleStatus
    check_in_time: Optional[datetime] = None
    check_in_staff_id: Optional[int] = None
    queue_position: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ScheduleWithDetails(Schedule):
    candidate_name: Optional[str] = None
    venue_name: Optional[str] = None
    check_in_staff_name: Optional[str] = None

class ScheduleCheckIn(BaseModel):
    schedule_id: int
    staff_id: int

class VenueQueueStatus(BaseModel):
    venue_id: int
    venue_name: str
    current_candidate: Optional[str] = None
    waiting_count: int
    queue_list: List[dict]