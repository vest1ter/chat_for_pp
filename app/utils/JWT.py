import jwt
from datetime import datetime, timedelta, timezone
from core.config import settings
from fastapi import HTTPException, status
from pydantic import BaseModel


class UserRefresh(BaseModel):
    id: str
    username: str

def create_access_token(user_id, user_name):
    payload = {
        'sub': str(user_id),
        'username': user_name,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.access_token_exp_minutes),
        'iat': datetime.now(timezone.utc),
    }
    try:
        return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
    except Exception as e:
        raise ValueError(f"Failed to encode JWT: {e}")

def create_refresh_token(user_id, user_name) -> str:
    payload = {
        'sub': str(user_id),
        'username': user_name,
        'exp': datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_token_expire_days),
        'iat': datetime.now(timezone.utc),
        'token_type': 'refresh',
    }
    try:
        return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
    except Exception as e:
        raise ValueError(f"Failed to encode refresh token: {e}")

def verify_token(token: str):
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        id = payload.get("sub")
        username = payload.get("username", None)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserRefresh(id=id, username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )