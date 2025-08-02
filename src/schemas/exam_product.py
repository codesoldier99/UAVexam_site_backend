from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ExamProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class ExamProductBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExamProductCreate(ExamProductBase):
    pass

class ExamProductRead(ExamProductBase):
    id: int
    status: ExamProductStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExamProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ExamProductStatus] = None

class ExamProductListResponse(BaseModel):
    items: List[ExamProductRead]
    total: int
    page: int
    size: int
    pages: int 