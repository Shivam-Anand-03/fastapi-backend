from fastapi import Response
from app.common.exceptions.base import UnprocessableEntity
from app.common.handlers import APIResponse
from .user_models import User
from .user_helper import UserHelper
from sqlmodel.ext.asyncio.session import AsyncSession
from .user_schema import UserCreate, UserLogin
from ...common.services.jwt_services import JwtServices
from ...common.settings import settings
from ...common.utils import CookieManager


class UserController:
    jwt_service = JwtServices(
        settings.ACCESS_TOKEN_SECRET_KEY, settings.REFRESH_TOKEN_SECRET_KEY
    )

    @classmethod
    async def signup_user_handler(cls, payload: UserCreate, session: AsyncSession):
        try:
            existing_user = await UserHelper.user_exists(payload.email, session)
            if existing_user:
                raise UnprocessableEntity("User with this email already exists.")

            user_data = payload.model_dump()
            user_data["password"] = UserHelper.hash_password(user_data["password"])

            new_user = User(**user_data)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            return APIResponse(message="User created successfully", data=new_user)

        except Exception as e:
            await session.rollback()
            raise UnprocessableEntity(f"Failed to create user: {str(e)}")

    @classmethod
    async def login_user_handler(
        cls, payload: UserLogin, session: AsyncSession, response: Response
    ):
        existing_user = await UserHelper.get_user_by_email(payload.email, session)
        if not existing_user:
            raise UnprocessableEntity(f"User does not exist with {payload.email} mail")

        is_correct_password = UserHelper.check_password(
            payload.password, existing_user.password
        )
        if not is_correct_password:
            raise UnprocessableEntity("Password provided is wrong")

        tokens = cls.jwt_service.create_tokens(
            user_data={"user_id": str(existing_user.id), "email": existing_user.email}
        )

        CookieManager.set_jwt_cookies(response, tokens)

        return APIResponse(
            message="Login successful", data={"token_type": tokens["token_type"]}
        )
