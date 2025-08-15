from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.candidate import CandidateStatus

class CandidateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    id_card: str = Field(..., min_length=18, max_length=18, pattern=r'^\d{17}[\dXx]$')
    phone: Optional[str] = Field(None, pattern=r'^1[3-9]\d{9}$')
    email: Optional[str] = None
    institution_id: int
    exam_product_id: int
    notes: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    phone: Optional[str] = Field(None, pattern=r'^1[3-9]\d{9}$')
    email: Optional[str] = None
    status: Optional[CandidateStatus] = None
    notes: Optional[str] = None

class CandidateBatchImport(BaseModel):
    candidates: List[CandidateBase]

class Candidate(CandidateBase):
    id: int
    status: CandidateStatus
    wechat_openid: Optional[str] = None
    queue_number: Optional[int] = None
    current_venue_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class CandidateWithDetails(Candidate):
    institution_name: Optional[str] = None
    exam_product_name: Optional[str] = None
    current_venue_name: Optional[str] = None

class CandidateQRCode(BaseModel):
    candidate_id: int
    schedule_id: Optional[int] = None
    qr_code_data: str

class CandidateLogin(BaseModel):
    id_card: str = Field(..., min_length=18, max_length=18)