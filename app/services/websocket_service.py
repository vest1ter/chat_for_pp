from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, desc, insert
from app.models.models import Message, Chat, ChatMember
from fastapi import HTTPException
from fastapi import status
from datetime import datetime, timezone

async def send_private_message_websocket_service(user_id: str, chat_id: str, data: str, session: AsyncSession):
    message = Message(
        user_id=user_id,
        chat_id=chat_id,
        content=data,
        created_at=datetime.now(timezone.utc),
    )
    session.add(message)
    await session.commit()