from sqlmodel import Field, SQLModel, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False),
    )
    title: str
    author: str
    publisher: str | None = None
    page_count: int
    language: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )

    def __repr__(self):
        return f"<Book {self.title}>"
