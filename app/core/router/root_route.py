from fastapi import APIRouter
from app.modules.book.book_routes import book_router

root_router = APIRouter()
root_router.include_router(book_router)
