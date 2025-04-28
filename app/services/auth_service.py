from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
from app.models.models import User
from app.utils import hashing
from fastapi import HTTPException
from fastapi import  status
from datetime import datetime, timezone
from app.db import postgres_service


async def login_user(username: str, password: str, session: AsyncSession):
    user = await postgres_service.get_user_by_usename_from_db(username, session)

    if not user:
        return False
    if not hashing.verify_password(password, user.hashed_password):
        return False
    return user

async def register_user(username: str, email: str, password: str, session: AsyncSession):
    ifuser = await postgres_service.get_user_id_by_email_from_db(email, session)

    if ifuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exist")

    hashed_password=hashing.hash_password(password)
    await postgres_service.add_user_to_db(username, email, hashed_password, session)
    
