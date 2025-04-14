from sqlalchemy import Column
from sqlalchemy import UUID
import uuid
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import uuid



class Base(DeclarativeBase):
    __abstract__ = True  # Базовый класс не создаёт таблицу
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
