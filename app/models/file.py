'''
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class File(Base):
    __tablename__ = "files"

    message_id = Column(ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    file_url = Column(String, nullable=False)

    message = relationship("Message", back_populates="files")
'''