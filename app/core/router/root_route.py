from fastapi import APIRouter
from app.modules.book.book_routes import book_router
from app.modules.user.user_routes import user_router

root_router = APIRouter()
root_router.include_router(book_router)
root_router.include_router(user_router)
