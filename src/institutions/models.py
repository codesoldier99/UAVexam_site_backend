from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from src.db.base import Base


class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, comment="机构名称")
    code = Column(String(50), unique=True, nullable=True, comment="机构代码")
    contact_person = Column(String(50), nullable=True, comment="联系人")
    phone = Column(String(20), nullable=True, comment="联系电话")
    email = Column(String(100), nullable=True, comment="联系邮箱")
    address = Column(Text, nullable=True, comment="机构地址")
    description = Column(Text, nullable=True, comment="机构描述")
    status = Column(String(20), default="active", comment="状态：active/inactive")
    license_number = Column(String(100), nullable=True, comment="许可证号")
    business_scope = Column(Text, nullable=True, comment="经营范围")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间") 