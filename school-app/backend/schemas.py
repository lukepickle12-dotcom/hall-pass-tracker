from pydantic import BaseModel, EmailStr
from models import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserOut(BaseModel):
    email: str
    role: UserRole

    class Config:
        from_attributes = True
