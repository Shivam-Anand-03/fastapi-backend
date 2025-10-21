from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .book_controller import BookController
from .book_schema import BookCreate, BookUpdate, BookRead
from app.core.database import DatabaseConnect
from ...common.schemas import AuthenticatedUser
from ...core.guards import authenticate_user
from ...common.exceptions import RoleAccessException

book_router = APIRouter(prefix="/books", tags=["Books"])


@book_router.get("/", response_model=list[BookRead])
async def get_all_books(session: AsyncSession = Depends(DatabaseConnect.get_session)):
    return await BookController.get_all_books_handler(session)


@book_router.get("/{book_id}")
async def get_book(
    book_id: str,
    session: AsyncSession = Depends(DatabaseConnect.get_session),
):
    return await BookController.get_book_handler(book_id, session)


@book_router.post("/", response_model=BookRead)
async def create_book(
    payload: BookCreate,
    user: AuthenticatedUser = Depends(authenticate_user),
    session: AsyncSession = Depends(DatabaseConnect.get_session),
):
    if user.role != "USER":
        raise RoleAccessException(
            f"Role '{user.role}' does not have access. Required role: 'USER'."
        )

    return await BookController.create_book_handler(payload, user.user_id, session)


@book_router.put("/{book_id}")
async def update_book(
    book_id: str,
    payload: BookUpdate,
    session: AsyncSession = Depends(DatabaseConnect.get_session),
):
    return await BookController.update_book_handler(book_id, payload, session)


@book_router.delete("/{book_id}")
async def delete_book(
    book_id: str, session: AsyncSession = Depends(DatabaseConnect.get_session)
):
    return await BookController.delete_book_handler(book_id, session)
