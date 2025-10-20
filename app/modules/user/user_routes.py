from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .user_controller import UserController
from .user_schema import UserRead, UserUpdate, UserCreate
from app.core.database import DatabaseConnect

user_router = APIRouter(prefix="/user", tags=["Auth"])


@user_router.post("/signup", response_model=list[UserRead])
async def signup_user(
    payload: UserCreate, session: AsyncSession = Depends(DatabaseConnect.get_session)
):
    return await UserController.signup_user_handler(payload, session)
