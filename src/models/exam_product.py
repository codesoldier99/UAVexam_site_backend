from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Float
from sqlalchemy.sql import func
from src.db.base import Base
import enum

class ExamCategory(enum.Enum):
    VLOS = "VLOS"
    BVLOS = "BVLOS"

class ExamType(enum.Enum):
    MULTIROTOR = "MULTIROTOR"
    FIXED_WING = "FIXED_WING"
    VTOL = "VTOL"

class ExamClass(enum.Enum):
    AGRICULTURE = "AGRICULTURE"
    POWER_INSPECTION = "POWER_INSPECTION"
    FILM_PHOTOGRAPHY = "FILM_PHOTOGRAPHY"
    LOGISTICS = "LOGISTICS"

class ExamLevel(enum.Enum):
    PILOT = "PILOT"
    CAPTAIN = "CAPTAIN"
    INSTRUCTOR = "INSTRUCTOR"

class ExamProduct(Base):
    __tablename__ = "exam_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="产品名称")
    description = Column(Text, nullable=True, comment="产品描述")
    code = Column(String(50), unique=True, default="PROD_001", comment="产品代码")
    category = Column(Enum(ExamCategory), default=ExamCategory.VLOS, comment="考试类别")
    exam_type = Column(Enum(ExamType), default=ExamType.MULTIROTOR, comment="考试类型")
    exam_class = Column(Enum(ExamClass), default=ExamClass.AGRICULTURE, comment="考试等级")
    exam_level = Column(Enum(ExamLevel), default=ExamLevel.PILOT, comment="考试级别")
    duration_minutes = Column(Integer, default=120, comment="考试时长(分钟)")
    theory_pass_score = Column(Integer, default=80, comment="理论考试及格分数")
    practical_pass_score = Column(Integer, default=80, comment="实操考试及格分数")
    training_hours = Column(Integer, default=40, comment="培训时长(小时)")
    price = Column(Float, default=1000.0, comment="考试费用")
    training_price = Column(Float, default=2000.0, comment="培训费用")
    theory_content = Column(Text, nullable=True, comment="理论考试内容")
    practical_content = Column(Text, nullable=True, comment="实操考试内容")
    requirements = Column(Text, nullable=True, comment="考试要求")
    is_active = Column(Integer, default=1, comment="是否激活")
    status = Column(Enum('active', 'inactive', name='exam_product_status'), default='active', comment="状态")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间") 