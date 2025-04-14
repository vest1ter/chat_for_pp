from http.client import HTTPException
from urllib import request

from fastapi import APIRouter, Depends, Response, Request

from core.config import settings

from models.db_helper import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import User
from schemas.auth_schemas.auth_requests import LoginUserRequest
from schemas.auth_schemas.auth_responses import LoginUserResponse, RefreshUserResponse, MeUserResponse
from services import auth_service
from utils.JWT import create_access_token, create_refresh_token, verify_token
from utils.cookies import set_auth_cookie, set_cookie
import jwt




router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=LoginUserResponse)
async def auth(
    response: Response,
    request: LoginUserRequest,
    session: AsyncSession = Depends(get_session),
):
    user = await auth_service.login_user(request.username, request.password, session)
    if not user:
        raise HTTPException(status_code=405, detail="Incorrect username or password")
    print(user)
    access_token = create_access_token(user.id, user.username)
    refresh_token = create_refresh_token(user.id, user.username)

    set_auth_cookie(response, access_token, refresh_token)

    return LoginUserResponse(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=RefreshUserResponse)
async def auth_refresh(
    response: Response,
    request: Request,
):

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token found")
    try:
        user = verify_token(refresh_token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token2")

    access_token = create_access_token(user.id, user.username)
    set_cookie(response, "access_token", access_token, settings.jwt.access_token_exp_minutes * 60)

    return RefreshUserResponse(
        access_token=access_token,
        token_type="bearer",
    )

@router.get("/me", response_model=MeUserResponse)
async def auth_me(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status=401, detail="token not found")
    user = verify_token(access_token)
    return MeUserResponse(
        user_id=user.id,
        username=user.username,
    )