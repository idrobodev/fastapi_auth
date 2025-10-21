from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    CONSULTA = "CONSULTA"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# UserInDB ya no es necesario con SQLAlchemy, usamos UserModel directamente

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None