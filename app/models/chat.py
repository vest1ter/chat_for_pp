'''
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import BaseModel


class Chat(Base):
    __tablename__ = "chats"

    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    messages = relationship("Message", back_populates="chat")
    members = relationship("ChatMember", back_populates="chat")
'''