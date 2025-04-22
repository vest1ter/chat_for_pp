FROM python:3.13-slim

ENV PYTHONPATH=/app

WORKDIR /app

# Установка Poetry
RUN pip install --upgrade pip && \
    pip install poetry==1.8.2

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (включая uvicorn)
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi && \
    pip install uvicorn alembic  # Устанавливаем alembic

COPY . .

# Применяем миграции перед запуском приложения
CMD cd app && alembic upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000