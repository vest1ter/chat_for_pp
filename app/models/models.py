from sqlalchemy import Column, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base


class ChatMember(Base):
    __tablename__ = "chat_members"

    chat_id = Column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")




class Chat(Base):
    __tablename__ = "chats"

    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    messages = relationship("Message", back_populates="chat")
    members = relationship("ChatMember", back_populates="chat")





class File(Base):
    __tablename__ = "files"

    message_id = Column(ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    file_url = Column(String, nullable=False)

    message = relationship("Message", back_populates="files")


class Message(Base):
    __tablename__ = "messages"

    chat_id = Column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="messages")
    files = relationship("File", back_populates="message")



class User(Base):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    messages = relationship("Message", back_populates="user")
    chat_memberships = relationship("ChatMember", back_populates="user")