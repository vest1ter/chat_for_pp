from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request, HTTPException
from app.core.config import WebSocketConnectionManager
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_helper import get_session
from app.utils.JWT import verify_token
from app.services.websocket_service import send_private_message_websocket_service, update_user_online_status
from app.db.S3service import get_s3_client
import json
import base64
from uuid import uuid4



router = APIRouter(
    tags=["websocket"],
)
manager = WebSocketConnectionManager()

@router.websocket("/ws/private/{chat_id}")
async def send_private_message_websocket(
        websocket: WebSocket,
        chat_id:str,
        s3 = Depends(get_s3_client),
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

    await update_user_online_status(user.id, is_online=True, session=session)

    #общение

    try:
        while True:
            # Принимаем данные (может быть текст или файл)
            data = await websocket.receive()
            if data["type"] == "websocket.receive":
                message = json.loads(data["text"])
                if message["type"] == "text":
                    # Обработка текстового сообщения
                    data = message["content"]
                    await send_private_message_websocket_service(user.id, chat_id, data, session)
                elif message["type"] == "file":
                    # Обработка файла
                    file_data = base64.b64decode(message["content"])
                    file_name = message["filename"]
                    file_type = message["filetype"]
                    # Сохраняем во временный файл (или обрабатываем в памяти)
                    temp_path = f"/tmp/{uuid4()}_{file_name}"
                    with open(temp_path, "wb") as f:
                        f.write(file_data)
                    # Загружаем в S3
                    object_name = f"chats/{chat_id}/{uuid4()}_{file_name}"
                    await s3.upload_file(temp_path, object_name)
                    file_url = await s3.get_presigned_url(object_name)
                    # Сохраняем в БД
                    await save_file_message(
                        chat_id=chat_id,
                        file_url=object_name,  # Сохраняем ключ, а не полный URL
                        file_type=file_type,
                        file_name=file_name,
                        session=session
                    )
                    # Отправляем подтверждение клиенту
                    await websocket.send_json({
                        "type": "file_ack",
                        "file_url": file_url,
                        "file_name": file_name
                    })
    except WebSocketDisconnect:
        await manager.disconnect(websocket, chat_id)







