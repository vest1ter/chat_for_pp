from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
from app.models.models import User
from app.utils import hashing
from fastapi import HTTPException
from fastapi import  status
from datetime import datetime, timezone


async def login_user(username: str, password: str, session: AsyncSession):
    result = await session.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        return False
    if not hashing.verify_password(password, user.hashed_password):
        return False
    return user

async def register_user(username: str, email: str, password: str, session: AsyncSession):
    ifuser = await session.execute(
        select(User).where(User.email == email)
    )
    ifuser = ifuser.scalar_one_or_none()
    if ifuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in this chat")

    user = User(
        username=username,
        email=email,
        hashed_password=hashing.hash_password(password),
        created_at=datetime.now(timezone.utc)
    )
    session.add(user)
    await session.commit()
