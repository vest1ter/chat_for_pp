from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request
from core.config import WebSocketConnectionManager
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_helper import get_session
from utils.JWT import verify_token
from http.client import HTTPException



router = APIRouter(
    tags=["websocket"],
)
manager = WebSocketConnectionManager()

@router.websocket("/ws/private/{chat_id}")
async def send_private_message_websocket(
        websocket: WebSocket,
        chat_id:str,
        session: AsyncSession = Depends(get_session),
):
    await websocket.accept()

    access_token = websocket.cookies.get("access_token")
    if not access_token:
        await websocket.close(code=1008, reason="Token not found")
        return

    try:
        user = verify_token(access_token)
    except Exception as e:
        await websocket.close(code=1008, reason="Invalid token")
        return

    await manager.connect(websocket, chat_id, user.id)






    print(user)

