from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class InstitutionStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class InstitutionBase(BaseModel):
    name: str
    contact_person: str
    phone: str

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionRead(InstitutionBase):
    id: int
    status: InstitutionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InstitutionUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[InstitutionStatus] = None 