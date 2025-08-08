from pydantic import BaseModel, ConfigDict, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from src.models.exam_product import ExamCategory, ExamType, ExamClass, ExamLevel

class ExamProductStatus(str, Enum):
    """考试产品状态枚举"""
    active = "active"
    inactive = "inactive"

class ExamProductBase(BaseModel):
    """考试产品基础模式"""
    name: str = Field(..., min_length=1, max_length=100, description="产品名称")
    description: Optional[str] = Field(None, max_length=1000, description="产品描述")
    code: Optional[str] = Field(None, min_length=3, max_length=50, description="产品代码")
    category: Optional[ExamCategory] = Field(ExamCategory.VLOS, description="考试类别")
    exam_type: Optional[ExamType] = Field(ExamType.MULTIROTOR, description="考试类型")
    exam_class: Optional[ExamClass] = Field(ExamClass.AGRICULTURE, description="考试等级")
    exam_level: Optional[ExamLevel] = Field(ExamLevel.PILOT, description="考试级别")
    duration_minutes: Optional[int] = Field(120, ge=30, le=480, description="考试时长(分钟)")
    theory_pass_score: Optional[int] = Field(80, ge=0, le=100, description="理论考试及格分数")
    practical_pass_score: Optional[int] = Field(80, ge=0, le=100, description="实操考试及格分数")
    training_hours: Optional[int] = Field(40, ge=0, le=1000, description="培训时长(小时)")
    price: Optional[float] = Field(1000.0, ge=0, description="考试费用")
    training_price: Optional[float] = Field(2000.0, ge=0, description="培训费用")
    theory_content: Optional[str] = Field(None, description="理论考试内容")
    practical_content: Optional[str] = Field(None, description="实操考试内容")
    requirements: Optional[str] = Field(None, description="考试要求")

    @validator('price', 'training_price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('价格不能为负数')
        return v

class ExamProductCreate(ExamProductBase):
    """创建考试产品模式"""
    name: str = Field(..., min_length=1, max_length=100, description="产品名称，必填")
    code: str = Field(..., min_length=3, max_length=50, description="产品代码，必填且唯一")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "多旋翼无人机驾驶员考试",
                "description": "适用于多旋翼无人机的驾驶员资格考试",
                "code": "MULTI_PILOT_001",
                "category": "VLOS",
                "exam_type": "MULTIROTOR",
                "exam_class": "AGRICULTURE",
                "exam_level": "PILOT",
                "duration_minutes": 120,
                "theory_pass_score": 80,
                "practical_pass_score": 80,
                "training_hours": 40,
                "price": 1500.0,
                "training_price": 3000.0,
                "theory_content": "无人机法规、飞行原理、气象知识等",
                "practical_content": "起飞、悬停、降落、紧急处置等",
                "requirements": "年满18周岁，身体健康，无犯罪记录"
            }
        }

class ExamProductRead(ExamProductBase):
    """考试产品响应模式"""
    id: int
    is_active: int = Field(description="是否激活，1=激活，0=未激活")
    status: str = Field(description="产品状态")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        """确保与SQLAlchemy对象的兼容性，处理脏数据"""
        return cls(
            id=obj.id,
            name=obj.name or "未命名产品",
            description=obj.description,
            code=obj.code or f"PROD_{obj.id:03d}",  # 处理空代码
            category=obj.category,
            exam_type=obj.exam_type,
            exam_class=obj.exam_class,
            exam_level=obj.exam_level,
            duration_minutes=max(30, obj.duration_minutes or 30),  # 处理无效时长
            theory_pass_score=obj.theory_pass_score,
            practical_pass_score=obj.practical_pass_score,
            training_hours=obj.training_hours,
            price=obj.price,
            training_price=obj.training_price,
            theory_content=obj.theory_content,
            practical_content=obj.practical_content,
            requirements=obj.requirements,
            is_active=obj.is_active if obj.is_active is not None else 1,  # 处理NULL值
            status=obj.status or "active",  # 处理NULL状态
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )

class ExamProductUpdate(BaseModel):
    """更新考试产品模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="产品名称")
    description: Optional[str] = Field(None, max_length=1000, description="产品描述")
    code: Optional[str] = Field(None, min_length=3, max_length=50, description="产品代码")
    category: Optional[ExamCategory] = Field(None, description="考试类别")
    exam_type: Optional[ExamType] = Field(None, description="考试类型")
    exam_class: Optional[ExamClass] = Field(None, description="考试等级")
    exam_level: Optional[ExamLevel] = Field(None, description="考试级别")
    duration_minutes: Optional[int] = Field(None, ge=30, le=480, description="考试时长(分钟)")
    theory_pass_score: Optional[int] = Field(None, ge=0, le=100, description="理论考试及格分数")
    practical_pass_score: Optional[int] = Field(None, ge=0, le=100, description="实操考试及格分数")
    training_hours: Optional[int] = Field(None, ge=0, le=1000, description="培训时长(小时)")
    price: Optional[float] = Field(None, ge=0, description="考试费用")
    training_price: Optional[float] = Field(None, ge=0, description="培训费用")
    theory_content: Optional[str] = Field(None, description="理论考试内容")
    practical_content: Optional[str] = Field(None, description="实操考试内容")
    requirements: Optional[str] = Field(None, description="考试要求")
    status: Optional[ExamProductStatus] = Field(None, description="产品状态")

    @validator('price', 'training_price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('价格不能为负数')
        return v

class ExamProductQuery(BaseModel):
    """考试产品查询参数模式"""
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(10, ge=1, le=100, description="每页数量")
    search: Optional[str] = Field(None, description="搜索关键词")
    category: Optional[ExamCategory] = Field(None, description="考试类别筛选")
    exam_type: Optional[ExamType] = Field(None, description="考试类型筛选")
    exam_class: Optional[ExamClass] = Field(None, description="考试等级筛选")
    exam_level: Optional[ExamLevel] = Field(None, description="考试级别筛选")
    status: Optional[ExamProductStatus] = Field(None, description="状态筛选")
    min_price: Optional[float] = Field(None, ge=0, description="最低价格")
    max_price: Optional[float] = Field(None, ge=0, description="最高价格")
    sort_by: Optional[str] = Field("created_at", description="排序字段")
    sort_order: Optional[str] = Field("desc", description="排序方向: asc/desc")

class ExamProductListResponse(BaseModel):
    """考试产品列表响应模式"""
    success: bool = True
    message: str = "获取成功"
    data: List[ExamProductRead]
    pagination: Dict[str, Any] = Field(description="分页信息")
    filters: Dict[str, Any] = Field(description="筛选条件")
    
class ExamProductResponse(BaseModel):
    """单个考试产品响应模式"""
    success: bool = True
    message: str = "操作成功"
    data: ExamProductRead

class ExamProductBatchUpdate(BaseModel):
    """批量更新考试产品模式"""
    ids: List[int] = Field(..., min_items=1, description="产品ID列表")
    status: Optional[ExamProductStatus] = Field(None, description="批量更新状态")
    is_active: Optional[int] = Field(None, ge=0, le=1, description="批量更新激活状态")

class ExamProductStats(BaseModel):
    """考试产品统计信息模式"""
    total_products: int = Field(description="总产品数")
    active_products: int = Field(description="激活产品数")
    inactive_products: int = Field(description="未激活产品数")
    avg_price: float = Field(description="平均价格")
    avg_training_price: float = Field(description="平均培训价格")
    category_stats: Dict[str, int] = Field(description="类别统计")
    type_stats: Dict[str, int] = Field(description="类型统计")

class ExamProductStatsResponse(BaseModel):
    """考试产品统计响应模式"""
    success: bool = True
    message: str = "统计成功"
    data: ExamProductStats