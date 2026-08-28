from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str  # min 8 chars

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str
    name: str
    avatar_url: str | None
    provider: str
    created_at: datetime

class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    mode: str
    created_at: datetime
    updated_at: datetime
    message_count: int
