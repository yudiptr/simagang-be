from app.utils.databases import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, event, func, Numeric, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=func.now())
    fullname = Column(String)
    student_number = Column(String, CheckConstraint('student_number ~ \'^[0-9]+$\'', name='student_number_check'))
    ipk = Column(Numeric(precision=3, scale=2, asdecimal=False), CheckConstraint('ipk >= 0 AND ipk <= 4', name='ipk_range_check'))
    phone_number = Column(String, CheckConstraint("phone_number ~ '^\+?[0-9]+$'", name='phone_number_check'))
    university = Column(String)
    semester = Column(Integer, CheckConstraint('semester >= 1 AND semester <= 12', name='semester_range_check'))


@event.listens_for(User, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now(timezone.utc)
