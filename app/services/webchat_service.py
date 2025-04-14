
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, desc
from models.models import Message
from http.client import HTTPException
#from logging import Logger

async def get_messages(chat_id:str, session: AsyncSession, limit: int = 50):
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



