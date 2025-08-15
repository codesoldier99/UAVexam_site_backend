from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Institution(Base):
    __tablename__ = "institutions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)  # 机构代码
    contact_person = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="institution")
    candidates = relationship("Candidate", back_populates="institution")