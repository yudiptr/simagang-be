import bcrypt
from app.utils.databases import Base
from datetime import datetime, timezone
from app.choices.role import Roles
from sqlalchemy import Column, DateTime, Integer, String, event, func, Boolean, Enum
from passlib.context import CryptContext
import hmac
import hashlib
from sqlalchemy import Column, DateTime, Integer, String, func, Boolean, Enum
from app.utils.databases import Base
from datetime import datetime, timezone
from app.choices.role import Roles
from app.config import Config

SECRET_KEY = Config.HASH_KEY.encode()

class UserAccount(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(Roles, name="roles"), default=Roles.USER, nullable=True)
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime, default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))

    def set_password(self, password):
        self.password = self.hash_password(password)

    def check_password(self, password):
        return hmac.compare_digest(self.password, self.hash_password(password))

    def hash_password(self, password):
        return hmac.new(SECRET_KEY, password.encode(), hashlib.sha256).hexdigest()
