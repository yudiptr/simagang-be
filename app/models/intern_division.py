from app.utils.databases import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, event, func, Numeric, CheckConstraint, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from app.choices.gender import Genders
from sqlalchemy.orm import relationship

class InternDivision(Base):
    __tablename__ = "intern_division"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=func.now())
    division_name = Column(String)
    
    # Define relationship with InternQuota
    quotas = relationship("InternQuota", back_populates="division")

@event.listens_for(InternDivision, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now(timezone.utc)
