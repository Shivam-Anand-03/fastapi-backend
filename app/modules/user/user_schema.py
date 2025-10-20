from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid


class UserCreate(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    username: str = Field(..., max_length=40)
    email: EmailStr
    password: str = Field(..., min_length=12)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    username: Optional[str] = Field(None, max_length=40)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_verified: Optional[bool] = None


class UserRead(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
