from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.db.base import Base


class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, comment="机构名称")
    contact_person = Column(String(50), nullable=True, comment="联系人")
    phone = Column(String(20), nullable=True, comment="联系电话")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间") 