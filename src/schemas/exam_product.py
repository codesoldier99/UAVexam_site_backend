from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
from src.models.exam_product import ExamCategory, ExamType, ExamClass, ExamLevel

class ExamProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class ExamProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    code: Optional[str] = None
    category: Optional[ExamCategory] = ExamCategory.VLOS
    exam_type: Optional[ExamType] = ExamType.MULTIROTOR
    exam_class: Optional[ExamClass] = ExamClass.AGRICULTURE
    exam_level: Optional[ExamLevel] = ExamLevel.PILOT
    duration_minutes: Optional[int] = 120
    theory_pass_score: Optional[int] = 80
    practical_pass_score: Optional[int] = 80
    training_hours: Optional[int] = 40
    price: Optional[float] = 1000.0
    training_price: Optional[float] = 2000.0
    theory_content: Optional[str] = None
    practical_content: Optional[str] = None
    requirements: Optional[str] = None

class ExamProductCreate(ExamProductBase):
    pass

class ExamProductRead(ExamProductBase):
    id: int
    is_active: Optional[int] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ExamProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    category: Optional[ExamCategory] = None
    exam_type: Optional[ExamType] = None
    exam_class: Optional[ExamClass] = None
    exam_level: Optional[ExamLevel] = None
    duration_minutes: Optional[int] = None
    theory_pass_score: Optional[int] = None
    practical_pass_score: Optional[int] = None
    training_hours: Optional[int] = None
    price: Optional[float] = None
    training_price: Optional[float] = None
    theory_content: Optional[str] = None
    practical_content: Optional[str] = None
    requirements: Optional[str] = None
    status: Optional[str] = None

class ExamProductListResponse(BaseModel):
    items: List[ExamProductRead]
    total: int
    page: int
    size: int
    pages: int 