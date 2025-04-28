from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, desc, insert
from app.models.models import Message, Chat, ChatMember
from fastapi import HTTPException
from fastapi import status
from datetime import datetime, timezone
from app.db.postgres_service import send_private_message_websocket_to_db, update_user_online_status_in_db

async def send_private_message_websocket_service(user_id: str, chat_id: str, data: str, session: AsyncSession):
    await send_private_message_websocket_to_db(user_id, chat_id, data, session)


async def update_user_online_status(user_id: str, is_online: bool, session: AsyncSession):
    await update_user_online_status_in_db(user_id, is_online, session)