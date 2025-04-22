from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from logging import getLogger
from typing import List

from fastapi import WebSocket, WebSocketDisconnect


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        #await websocket.accept()
        self.active_connections.append(
            {"websocket": websocket, "room_id": room_id, "user_id": user_id}
        )

    def disconnect(self, websocket: WebSocket, room_id: str):
        self.active_connections = [
            conn
            for conn in self.active_connections
            if not (conn["websocket"] == websocket and conn["room_id"] == room_id)
        ]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, message: str, room_id: str):
        for connection in self.active_connections:
            if connection["room_id"] == room_id:
                await connection["websocket"].send_text(message)


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class S3Config(BaseModel):
    endpoint_url: str
    root_user: str
    root_password: str
    bucket_name: str

class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_exp_minutes: int
    refresh_token_expire_days: int



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    S3: S3Config
    jwt: JWTConfig




settings = Settings()
