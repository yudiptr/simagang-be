from app.utils.databases import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, event, func, Numeric, CheckConstraint, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.choices.gender import Genders
from app.choices.intern_registration_status import InternRegistrationStatus

class InternRegistration(Base):
    __tablename__ = "intern_registration"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime, default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))
    status = Column(Enum(InternRegistrationStatus, name="intern_registration_status"), nullable=False, default=InternRegistrationStatus.ON_PROCESS)
    cv = Column(String)
    cover_letter = Column(String)
    student_card = Column(String)
    photo = Column(String)
    proposal = Column(String)
    updated_with = Column(String)
    duration = Column(String)
    division_id = Column(Integer, ForeignKey('intern_division.id'))
    user_account_id = Column(Integer, ForeignKey("user_account.id"))
