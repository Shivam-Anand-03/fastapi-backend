from sqlmodel import Field, SQLModel, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False),
    )

    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    is_verified: bool = Field(default=False)
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="USER")
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )

    def __repr__(self):
        return f"<User {self.email}>"
