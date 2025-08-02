from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class InstitutionBase(BaseModel):
    name: str
    code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "active"
    license_number: Optional[str] = None
    business_scope: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    # 创建机构时包含初始登录账号信息
    admin_username: str
    admin_email: EmailStr
    admin_password: str


class InstitutionRead(InstitutionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InstitutionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    license_number: Optional[str] = None
    business_scope: Optional[str] = None


class InstitutionListResponse(BaseModel):
    items: List[InstitutionRead]
    total: int
    page: int
    size: int
    pages: int


class InstitutionStats(BaseModel):
    total_institutions: int
    active_institutions: int
    inactive_institutions: int
    total_users: int 