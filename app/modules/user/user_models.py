from sqlmodel import Field, SQLModel, Column, String, ForeignKey, Relationship
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False),
    )
    name: str = Field(sa_column=Column(String, unique=True, nullable=False))
    description: str | None = Field(
        default=None, sa_column=Column(String, nullable=True)
    )

    users: list["User"] = Relationship(back_populates="role")


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

    role_id: uuid.UUID | None = Field(
        default=None,
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True),
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

    role: Role | None = Relationship(back_populates="users")

    def __repr__(self):
        return f"<User {self.email}>"
