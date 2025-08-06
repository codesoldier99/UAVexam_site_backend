from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from src.db.base import Base


class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="考场名称")
    type = Column(String(50), nullable=False, comment="考场类型（理论、实操、候考）")
    address = Column(String(255), nullable=True, comment="考场地址")
    description = Column(Text, nullable=True, comment="考场描述")
    capacity = Column(Integer, nullable=False, default=0, comment="容纳人数")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")
    status = Column(String(20), default='active', nullable=False, comment="状态(active/inactive)")
    contact_person = Column(String(50), nullable=True, comment="联系人")
    contact_phone = Column(String(20), nullable=True, comment="联系电话")
    equipment_info = Column(Text, nullable=True, comment="设备信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Venue(id={self.id}, name='{self.name}', type='{self.type}', capacity={self.capacity})>" 