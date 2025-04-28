from http.client import HTTPException


from fastapi import APIRouter, Depends, Response, Request, Query

from app.core.config import settings
from typing import Optional
from app.models.db_helper import get_session
from app.schemas.webchat_schemas.webchat_responses import CreatePrivateChatResponse, GetOnlineStatusResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User
from app.services import webchat_service
from app.utils.JWT import verify_token
from app.utils.cookies import set_auth_cookie, set_cookie
import jwt

from db import postgres_service

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)



@router.get("/get_messages")
async def get_messages_api(
        request: Request,
        chat_id: str,
        session: AsyncSession = Depends(get_session)):
    access_token = request.cookies.get("access_token")
    if not access_token: raise HTTPException(401)
    user = verify_token(access_token)

    last_messages = await webchat_service.get_messages(user, chat_id, session)

    return last_messages


@router.post("/private_message")
async def send_private_message_api(
        request: Request,
        response: Response,
        chat_id: str,
        text_data: str,
        session: AsyncSession = Depends(get_session)
):
    access_token = request.cookies.get("access_token")
    if not access_token: raise HTTPException(401)
    user = verify_token(access_token)

    await webchat_service.send_private_message(user, chat_id, text_data, session)

    return {"success": True}

@router.post("/create_private_chat", response_model=CreatePrivateChatResponse)
async def create_chat(
        to_user_email: str,
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    access_token = request.cookies.get("access_token")
    if not access_token: raise HTTPException(401)
    current_user = verify_token(access_token)

    to_user = await webchat_service.get_user_id_by_email(to_user_email, session)
    print(to_user.id)

    chat_name = f"{current_user.username}_{to_user.username}"

    print(chat_name)

    chat_id = await webchat_service.exist_chat(chat_name, session)
    print(chat_id)
    if chat_id is None: chat_id = await webchat_service.create_private_chat(chat_name, current_user, to_user, session)
    print(chat_id)

    return CreatePrivateChatResponse(
        chat_id=str(chat_id),
        chat_name=chat_name,
        current_user=current_user.username,
        to_user=to_user.username,
    )

@router.get("/get_online_status", response_model=GetOnlineStatusResponse)
async def get_online_status(
        user_email: str,
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    access_token = request.cookies.get("access_token")
    if not access_token: raise HTTPException(401)

    status = await webchat_service.get_online_status(user_email, session)

    return GetOnlineStatusResponse(
        user_email=user_email,
        is_online=status,
    )
