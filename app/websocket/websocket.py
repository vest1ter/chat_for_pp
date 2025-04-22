from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request, HTTPException
from app.core.config import WebSocketConnectionManager
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_helper import get_session
from app.utils.JWT import verify_token
from app.services.websocket_service import send_private_message_websocket_service



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

    #общение
    try:
        while True:
            data = await websocket.receive_text()
            await send_private_message_websocket_service(user.id, chat_id, data, session)
            await manager.broadcast_message(
                f"{user.username}: {data}", chat_id
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
        await manager.broadcast_message(
            f"User {user.username} left the private chat", chat_id
        )






    print(user)

