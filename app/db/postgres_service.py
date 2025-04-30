from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, desc, insert, update
from app.models.models import Message, Chat, ChatMember, User
from datetime import datetime, timezone
import uuid
import logging
logger = logging.getLogger(__name__)


async def get_all_users_chats_from_db(user_id, session: AsyncSession):
    query = (
        select(Chat)
        .join(ChatMember, Chat.id == ChatMember.chat_id)
        .filter(ChatMember.user_id == user_id)
    )
    result = await session.execute(query)

    result = result.scalars().all()

    chats = [{"chat_id": chat.id,"chat_name": chat.name} for chat in result]

    logger.debug(chats)
    return chats


async def get_user_by_usename_from_db(username, session: AsyncSession):
    result = await session.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()

    return user

async def add_user_to_db(username, email, hashed_password, session):
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        created_at=datetime.now(timezone.utc)
    )
    session.add(user)
    await session.commit()


async def chek_membership_in_db(chat_id, user, session: AsyncSession):
    membership_result = await session.execute(
        select(ChatMember).where(ChatMember.chat_id == chat_id, ChatMember.user_id == user.id)
    )
    membership = membership_result.scalar_one_or_none()
    return membership

async def get_messages_from_db(chat_id, limit, session: AsyncSession):
    query = (
        select(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(desc(Message.created_at))
        .limit(limit)
    )

    result = await session.execute(query)
    result = result.scalars().all()
    return result

async def add_message_to_db(user, chat_id, text_data, session:AsyncSession):
    message = Message(
        user_id=user.id,
        chat_id=chat_id,
        content=text_data,
        created_at=datetime.now(timezone.utc)
    )
    session.add(message)
    await session.commit()


async def exist_chat_in_db(chat_name, session: AsyncSession):
    query = select(Chat).filter(Chat.name == chat_name)
    chat = await session.execute(query)
    chat = chat.scalars().first()
    if chat is None:
        return None
    return chat.id


async def create_chat_in_db(chat_name, session: AsyncSession):
    chat_id = str(uuid.uuid4())
    chat = Chat(
        id=chat_id,
        name=chat_name,
        created_at=datetime.now(timezone.utc),
    )
    session.add(chat)
    await session.commit()

    return chat_id

async def add_member_to_chat_in_db(chat_id, user, session: AsyncSession):
    member = ChatMember(
        chat_id=chat_id,
        user_id=user.id,
        joined_at=datetime.now(timezone.utc),
    )

    session.add(member)
    await session.commit()

async def get_user_id_by_email_from_db(email, session: AsyncSession):
    
    query = (select(User).filter(User.email == email))

    result = await session.execute(query)
    user = result.scalars().first()

    return user

async def send_private_message_websocket_to_db(user_id: str, chat_id: str, data: str, session: AsyncSession):
    message = Message(
        user_id=user_id,
        chat_id=chat_id,
        content=data,
        created_at=datetime.now(timezone.utc),
    )
    session.add(message)
    await session.commit()

async def update_user_online_status_in_db(user_id: str, is_online: bool, session: AsyncSession):
    stmt = (
        update(User)
        .filter(User.id == user_id)
        .values(is_active=is_online)
    )
    await session.execute(stmt)
    await session.commit()

async def get_online_status(user_email: str, session: AsyncSession):
    query = (select(User).filter(User.email == user_email))

    result = await session.execute(query)
    user = result.scalars().first()

    return user.is_active