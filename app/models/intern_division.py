from app.utils.databases import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, event, func, Numeric, CheckConstraint, Enum, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from app.choices.gender import Genders
from sqlalchemy.orm import relationship

class InternDivision(Base):
    __tablename__ = "intern_division"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime, default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))
    is_deleted = Column(Boolean, default=False)
    division_name = Column(String, unique= True, nullable=False)
    
    # Define relationship with InternQuota
    quotas = relationship("InternQuota", back_populates="division")
