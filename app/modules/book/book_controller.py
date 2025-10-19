from sqlmodel.ext.asyncio.session import AsyncSession
from .book_schema import BookCreate, BookUpdate, BookRead
from sqlmodel import select, desc
from .book_models import Book
from app.common.exceptions.base import NotFoundException, UnprocessableEntity
from app.common.handlers import APIResponse


class BookController:

    @staticmethod
    async def get_all_books(session: AsyncSession) -> list[BookRead]:
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def get_book(book_id: str, session: AsyncSession) -> Book:
        if not book_id:
            raise NotFoundException("Book ID is required")

        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        book = result.first()
        if not book:
            raise NotFoundException(f"Book with id {book_id} not found")
        return book

    @staticmethod
    async def create_book(data: BookCreate, session: AsyncSession) -> BookRead:
        try:
            new_book = Book(**data.model_dump())
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
            return new_book
        except Exception as e:
            await session.rollback()
            raise UnprocessableEntity(f"Failed to create book: {str(e)}")

    @staticmethod
    async def update_book(
        book_id: str, data: BookUpdate, session: AsyncSession
    ) -> BookRead:
        book_to_update = await BookController.get_book(book_id, session)

        try:
            update_data_dict = data.model_dump(exclude_unset=True)
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)

            await session.commit()
            await session.refresh(book_to_update)

            return book_to_update
        except Exception as e:
            await session.rollback()
            raise UnprocessableEntity(f"Failed to update book: {str(e)}")

    @staticmethod
    async def delete_book(book_id: str, session: AsyncSession):
        book_to_delete = await BookController.get_book(book_id, session)

        try:
            await session.delete(book_to_delete)
            await session.commit()
            return APIResponse("Book deleted successfully")
        except Exception as e:
            await session.rollback()
            raise UnprocessableEntity(f"Failed to delete book: {str(e)}")
