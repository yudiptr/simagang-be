from app.utils.databases import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, event, func, Numeric, CheckConstraint, Enum, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.choices.gender import Genders

class InternQuota(Base):
    __tablename__ = "intern_quota"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=func.now())
    duration = Column(String)
    quota = Column(Integer)
    is_deleted = Column(Boolean, default = False)
    
    # Define foreign key relationship with InternDivision
    division_id = Column(Integer, ForeignKey('intern_division.id'))
    division = relationship("InternDivision", back_populates="quotas")

@event.listens_for(InternQuota, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now(timezone.utc)
