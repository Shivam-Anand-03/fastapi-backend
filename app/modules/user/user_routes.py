from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from .user_controller import UserController
from .user_schema import UserCreate, UserLogin
from app.core.database import DatabaseConnect

user_router = APIRouter(prefix="/user", tags=["Auth"])


@user_router.post("/signup")
async def signup_user(
    payload: UserCreate, session: AsyncSession = Depends(DatabaseConnect.get_session)
):
    return await UserController.signup_user_handler(payload, session)


@user_router.post("/login")
async def login_user(
    payload: UserLogin,
    response: Response,
    session: AsyncSession = Depends(DatabaseConnect.get_session),
):
    return await UserController.login_user_handler(payload, session, response)
