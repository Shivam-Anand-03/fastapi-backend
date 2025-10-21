from sqlmodel import Field, SQLModel, Column, Relationship
from typing import Optional, TYPE_CHECKING
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.modules.user.user_models import User


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False),
    )
    title: str
    author: str
    publisher: Optional[str] = None
    page_count: int
    language: str

    user_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            pg.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
        ),
    )
    user: Optional["User"] = Relationship(back_populates="books")

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )
