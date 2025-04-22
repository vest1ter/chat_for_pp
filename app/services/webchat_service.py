
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, desc, insert
from app.models.models import Message, Chat, ChatMember, User
from fastapi import HTTPException
from fastapi import status
from datetime import datetime, timezone
import uuid
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

async def create_private_chat(chat_name: str, current_user, to_user, session: AsyncSession):

    chat_id = str(uuid.uuid4())
    chat = Chat(
        id=chat_id,
        name=chat_name,
        created_at=datetime.now(timezone.utc),
    )
    session.add(chat)
    await session.commit()

    member_one = ChatMember(
        chat_id=chat_id,
        user_id=current_user.id,
        joined_at=datetime.now(timezone.utc),
    )
    member_two = ChatMember(
        chat_id=chat_id,
        user_id=to_user.id,
        joined_at=datetime.now(timezone.utc),
    )
    session.add_all([member_one, member_two])
    await session.commit()

    return chat_id



async def get_user_id_by_email(email: str, session: AsyncSession):
    query = (select(User).filter(User.email == email))

    result = await session.execute(query)
    user = result.scalars().first()

    if not user: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    return user