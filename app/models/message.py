'''
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base


class Message(Base):
    __tablename__ = "messages"

    chat_id = Column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="messages")
    files = relationship("File", back_populates="message")
'''