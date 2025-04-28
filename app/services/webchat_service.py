
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, desc, insert
from app.models.models import Message, Chat, ChatMember, User
from fastapi import HTTPException
from fastapi import status
from datetime import datetime, timezone
import uuid
from app.db import postgres_service
#from logging import Logger

async def get_messages(user: str, chat_id:str, session: AsyncSession, limit: int = 50):
    membership = await postgres_service.chek_membership_in_db(chat_id, user, session)
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in this chat")

    messages = await postgres_service.get_messages_from_db(chat_id, limit, session)

    if not messages: raise HTTPException(401)

    return messages


async def send_private_message(user, chat_id, text_data, session: AsyncSession):
    membership = await postgres_service.chek_membership_in_db(chat_id, user, session)
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in this chat")

    await postgres_service.add_message_to_db(user, chat_id, text_data, session)


async def exist_chat(chat_name: str, session: AsyncSession):
    chat_id = await postgres_service.exist_chat_in_db(chat_name, session)
    return chat_id


async def create_private_chat(chat_name: str, current_user, to_user, session: AsyncSession):

    chat_id = await postgres_service.create_chat_in_db(chat_name, session)
    
    await postgres_service.add_member_to_chat_in_db(chat_id, current_user, session)
    await postgres_service.add_member_to_chat_in_db(chat_id, to_user, session)

    return chat_id



async def get_user_id_by_email(email: str, session: AsyncSession):
    
    user = await postgres_service.get_user_id_by_email_from_db(email, session)
    
    if not user: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    return user

async def get_online_status(user_email: str, session: AsyncSession):
    status = await postgres_service.get_online_status(user_email, session)

    return status