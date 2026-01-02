from pydantic import BaseModel, EmailStr
from .models import UserRole
import uuid


class LoginUserResponse(BaseModel):
    token: str
    token_type: str


class UserResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str | None
    email: EmailStr
    phone_number: str
    role: UserRole
