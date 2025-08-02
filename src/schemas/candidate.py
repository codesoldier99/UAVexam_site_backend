from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    id_number: str
    phone: str
    email: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[datetime] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    target_exam_product_id: Optional[int] = None
    institution_id: int
    exam_product_id: int
    status: Optional[str] = "待审核"
    notes: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    id_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[datetime] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    target_exam_product_id: Optional[int] = None
    institution_id: Optional[int] = None
    exam_product_id: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class CandidateRead(CandidateBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    # 兼容字段
    id_card: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class CandidateListResponse(BaseModel):
    items: List[CandidateRead]
    total: int
    page: int
    size: int
    pages: int

class BatchImportResponse(BaseModel):
    success_count: int
    failed_count: int
    errors: List[str] = [] 