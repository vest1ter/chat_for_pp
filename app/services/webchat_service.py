
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, desc, insert
from models.models import Message, Chat, ChatMember
from fastapi import HTTPException
from fastapi import status
from datetime import datetime, timezone
#from logging import Logger

async def get_messages(user: str, chat_id:str, session: AsyncSession, limit: int = 50):
    membership_result = await session.execute(
        select(ChatMember).where(ChatMember.chat_id == chat_id, ChatMember.user_id == user.id)
    )
    membership = membership_result.scalar_one_or_none()
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in this chat")

    query = (
        select(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(desc(Message.created_at))
        .limit(limit)
    )

    result = await session.execute(query)
    result = result.scalars().all()

    if not result: raise HTTPException(401)

    return result


async def send_private_message(user, chat_id, text_data, session: AsyncSession):
    membership_result = await session.execute(
        select(ChatMember).where(ChatMember.chat_id == chat_id, ChatMember.user_id == user.id)
    )
    membership = membership_result.scalar_one_or_none()
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in this chat")


    message = Message(
        user_id=user.id,
        chat_id=chat_id,
        content=text_data,
        created_at=datetime.now(timezone.utc)
    )
    session.add(message)
    await session.commit()

