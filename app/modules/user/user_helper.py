from passlib.hash import pbkdf2_sha256
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.common.exceptions.base import UnprocessableEntity
from app.modules.user.user_models import User
from .user_schema import UserRead
from typing import Optional


class UserHelper:
    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession) -> Optional["User"]:
        """Fetch a user by email."""
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_user_by_id(user_id: str, session: AsyncSession) -> Optional["User"]:
        """Fetch a user by id."""
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def user_exists(email: str, session: AsyncSession) -> bool:
        """Check if a user with this email already exists."""
        if not email:
            raise UnprocessableEntity("Email is required.")
        user = await UserHelper.get_user_by_email(email, session)
        return user is not None

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password securely using PBKDF2."""
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """Verify a password against a stored hash."""
        return pbkdf2_sha256.verify(password, hashed_password)
