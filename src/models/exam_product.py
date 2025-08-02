from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from src.db.base import Base
import enum

class ExamCategory(enum.Enum):
    VLOS = "vlos"
    BVLOS = "bvlos"
    NIGHT = "night"

class ExamType(enum.Enum):
    MULTIROTOR = "multirotor"
    FIXED_WING = "fixed_wing"
    HELICOPTER = "helicopter"

class ExamClass(enum.Enum):
    AGRICULTURE = "agriculture"
    SURVEY = "survey"
    TRANSPORT = "transport"

class ExamLevel(enum.Enum):
    PILOT = "pilot"
    INSTRUCTOR = "instructor"
    EXAMINER = "examiner"

class ExamProduct(Base):
    __tablename__ = "exam_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="产品名称")
    description = Column(String(255), nullable=True, comment="产品描述")
    status = Column(Enum('active', 'inactive', name='exam_product_status'), default='active', comment="状态")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间") 