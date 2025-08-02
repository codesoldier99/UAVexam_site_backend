from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    id_card: str
    institution_id: int
    exam_product_id: int
    status: str = "待排期"

class CandidateCreate(CandidateBase):
    pass

class CandidateRead(CandidateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    # 关联信息
    institution_name: Optional[str] = None
    exam_product_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    id_card: Optional[str] = None
    institution_id: Optional[int] = None
    exam_product_id: Optional[int] = None
    status: Optional[str] = None

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