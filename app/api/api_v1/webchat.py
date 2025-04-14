from http.client import HTTPException


from fastapi import APIRouter, Depends, Response, Request

from core.config import settings

from models.db_helper import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import User
from services import webchat_service
from utils.JWT import verify_token
from utils.cookies import set_auth_cookie, set_cookie
import jwt

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)



@router.get("/messages")
async def get_messages(
        request: Request,
        chat_id: str,
        session: AsyncSession = Depends(get_session)):
    access_token = request.cookies.get("access_token")
    if not access_token: raise HTTPException(401)
    user = verify_token(access_token)
    last_messages = await webchat_service.get_messages(chat_id, session)

    return last_messages





