from http.client import HTTPException


from fastapi import APIRouter, Depends, Response, Request

from app.core.config import settings

from app.models.db_helper import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User
from app.services import webchat_service
from app.utils.JWT import verify_token
from app.utils.cookies import set_auth_cookie, set_cookie
import jwt

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
    user = verify_token(access_token)

    await webchat_service.send_private_message(user, chat_id, text_data, session)

    return {"success": True}


