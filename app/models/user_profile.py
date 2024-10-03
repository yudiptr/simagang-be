from app.utils.databases import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, event, func, Numeric, CheckConstraint, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from app.choices.gender import Genders

class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime, default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))
    fullname = Column(String)
    student_number = Column(String, CheckConstraint('student_number ~ \'^[0-9]+$\'', name='student_number_check'))
    ipk = Column(Numeric(precision=3, scale=2, asdecimal=False), CheckConstraint('ipk >= 0 AND ipk <= 4', name='ipk_range_check'))
    phone_number = Column(String, CheckConstraint("phone_number ~ '^\+?[0-9]+$'", name='phone_number_check'))
    university = Column(String)
    semester = Column(Integer, CheckConstraint('semester >= 1 AND semester <= 12', name='semester_range_check'))
    gender = Column(Enum(Genders, name="gender_choices"), nullable=True)
    email = Column(String)
    user_account_id = Column(Integer, ForeignKey('user_account.id'), nullable=False, unique=True)
