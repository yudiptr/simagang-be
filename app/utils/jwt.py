from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt
from app.config import Config
from fastapi import HTTPException, status


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET, algorithm=Config.JWT_HASH_METHOD)
    return encoded_jwt


def extract_jwt(auth_token):
    try:
        token_data = jwt.decode(auth_token, Config.JWT_SECRET, algorithms=[Config.JWT_HASH_METHOD])
        return token_data
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid token: {e}")
    