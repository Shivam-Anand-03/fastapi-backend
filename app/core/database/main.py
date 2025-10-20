from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.common.settings import settings


class DatabaseConnect:
    """
    Async database connection using SQLModel + SQLAlchemy.
    """

    engine = create_async_engine(
        url=settings.DATABASE_URL,
        echo=True,
    )

    # ✅ Use SQLModel's AsyncSession here
    SessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
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
