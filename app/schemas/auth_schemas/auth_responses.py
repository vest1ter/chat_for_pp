from pydantic import BaseModel

class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class RefreshUserResponse(BaseModel):
    access_token: str
    token_type: str

class MeUserResponse(BaseModel):
    user_id: str
    username: str

class RegisterUserResponse(BaseModel):
    username: str