from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class BookBase(BaseModel):
    title: str
    author: str
    publisher: Optional[str] = None
    page_count: int
    language: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None


class BookRead(BookBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
