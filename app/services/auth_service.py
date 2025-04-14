from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
from models.models import User
from utils import hashing


async def login_user(username: str, password: str, session: AsyncSession):
    result = await session.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        return False
    if not hashing.verify_password(password, user.hashed_password):
        return False
    return user

