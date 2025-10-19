from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.common.settings import settings
from app.modules.book.book_models import Book
from sqlalchemy.ext.asyncio import create_async_engine


class DatabaseConnect:
    """
    Async database connection using SQLModel + SQLAlchemy.
    """

    engine = create_async_engine(
        url=settings.DATABASE_URL,
        echo=True,
    )

    # Async session factory
    SessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    @classmethod
    async def init_db(cls) -> None:
        async with cls.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("✅ Database initialized successfully.")

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """
        Async generator for database sessions
        """
        async with cls.SessionLocal() as session:
            yield session
