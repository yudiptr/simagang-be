import bcrypt
from app.utils.databases import Base
from datetime import datetime, timezone
from app.choices.role import Roles
from sqlalchemy import Column, DateTime, Integer, String, event, func, Boolean, Enum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserAccount(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(Roles, name="roles"), default=Roles.USER, nullable=True)
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=func.now())

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

@event.listens_for(UserAccount, 'before_insert', propagate=True)
def receive_before_insert(mapper, connection, target):
    target.set_password(target.password)

@event.listens_for(UserAccount, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    if target.password:
        target.set_password(target.password)
    target.updated_at = datetime.now(timezone.utc)
