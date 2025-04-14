from pydantic import BaseModel

class LoginUserRequest(BaseModel):
    username: str
    password: str
