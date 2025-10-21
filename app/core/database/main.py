import logging

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.common.settings import settings
from sqlalchemy import text


class DatabaseConnect:
    """
    Async database connection using SQLModel + SQLAlchemy.
    Alembic handles migrations; no need for create_all().
    """

    engine = create_async_engine(
        url=settings.DATABASE_URL,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    @classmethod
    async def test_connection(cls) -> None:
        """
        Test DB connection and print success only if reachable.
        """
        try:
            async with cls.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            print("✅ Database connection successful.")
        except SQLAlchemyError as e:
            print(f"❌ Failed to connect to database: {e}")

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """
        Async generator for database sessions
        """
        async with cls.SessionLocal() as session:
            yield session
