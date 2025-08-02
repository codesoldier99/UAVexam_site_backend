from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from src.db.base import Base


class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="考场名称")
    type = Column(String(50), nullable=False, comment="考场类型（理论、实操、候考）")
    status = Column(Enum('active', 'inactive', name='venue_status'), default='active', comment="状态")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间") 