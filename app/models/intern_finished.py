from app.utils.databases import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, event, func, Numeric, CheckConstraint, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.choices.gender import Genders
from app.choices.intern_registration_status import InternRegistrationStatus

class InternFinished(Base):
    __tablename__ = "intern_finished"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    intern_certification = Column(String)
    division_id = Column(Integer, ForeignKey('intern_division.id'))
    user_account_id = Column(Integer, ForeignKey("user_account.id"))
