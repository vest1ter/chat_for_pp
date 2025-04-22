from pydantic import BaseModel

class LoginUserRequest(BaseModel):
    username: str
    password: str

class RegisterUserRequest(BaseModel):
    username: str
    email: str
    password: str
    repeat_password: str
