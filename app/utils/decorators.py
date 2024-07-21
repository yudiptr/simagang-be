from fastapi import Request, status, HTTPException
from functools import wraps
import jwt
from jwt.exceptions import InvalidTokenError
from app.utils.jwt import extract_jwt
from typing import Any, Callable, List
from app.config import Config

def login_required(
    token_types: List[str] = ["USER", "Admin"],
    return_validation_data: bool = False
) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        async def wrapper(*args, **kwargs) -> Any:
            request: Request = kwargs.get("request")
            auth_token = request.headers.get("Authorization", request.headers.get("authorization"))

            if not auth_token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

            token_data = extract_jwt(auth_token[7:])            

            allowed_token_types = token_types
            if "role" in token_data and token_data["role"] not in allowed_token_types:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid role")

            if return_validation_data:
                kwargs["validation_data"] = token_data

            return await f(*args, **kwargs)

        return wrapper

    return decorator
