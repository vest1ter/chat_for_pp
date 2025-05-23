from pydantic import BaseModel

class CreatePrivateChatResponse(BaseModel):
    chat_id: str
    chat_name: str
    current_user: str
    to_user: str

class GetOnlineStatusResponse(BaseModel):
    user_email: str
    is_online: bool