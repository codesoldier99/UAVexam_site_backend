from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InstitutionBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionRead(InstitutionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InstitutionUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None 