from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class VenueStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class VenueBase(BaseModel):
    name: str
    type: str

class VenueCreate(VenueBase):
    pass

class VenueRead(VenueBase):
    id: int
    status: VenueStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VenueUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[VenueStatus] = None

class VenueListResponse(BaseModel):
    items: List[VenueRead]
    total: int
    page: int
    size: int
    pages: int 