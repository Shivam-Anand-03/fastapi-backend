from fastapi import Response, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from ...common.exceptions.base import (
    UnprocessableEntity,
    TokenInavlidException,
)
from sqlalchemy.orm import selectinload
from sqlmodel import select, desc
from ...common.handlers import APIResponse
from .user_models import User
from .user_helper import UserHelper
from .user_schema import UserCreate, UserLogin, UserRead
from ...common.services.jwt_services import JwtServices
from ...common.settings import settings
from ...common.utils import CookieManager
from ...common.schemas import SessionModel


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

            return APIResponse(
                message="User created successfully",
                data={
                    "id": str(new_user.id),
                    "email": new_user.email,
                    "role": new_user.role,
                },
            )

        except UnprocessableEntity as ue:
            raise ue
        except Exception as e:
            raise UnprocessableEntity(f"Failed to create user: {str(e)}")

    @classmethod
    async def login_user_handler(
        cls, payload: UserLogin, session: AsyncSession, response: Response
    ):
        existing_user = await UserHelper.get_user_by_email(payload.email, session)
        if not existing_user:
            raise UnprocessableEntity(f"User does not exist with {payload.email} email")

        is_correct_password = UserHelper.check_password(
            payload.password, existing_user.password
        )
        if not is_correct_password:
            raise UnprocessableEntity("Password provided is wrong")

        user_session = SessionModel(
            user_id=str(existing_user.id),
            email=existing_user.email,
            role=existing_user.role,
        )

        tokens = cls.jwt_service.create_tokens(user_data=user_session)

        CookieManager.set_jwt_cookies(response, tokens)

        return APIResponse(
            message="Login successful", data={"acess_token": tokens["access_token"]}
        )

    @classmethod
    async def refresh_token_handler(cls, request: Request, response: Response):
        token = request.cookies.get("refresh_token")
        if not token:
            raise TokenInavlidException("Refresh token not found.")

        decoded = cls.jwt_service.decode_token(token, token_type="refresh")
        payload = decoded.get("payload")
        print(payload)

        user_id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")
        if not user_id or not email or not role:
            raise TokenInavlidException("Invalid token payload.")

        user_session = SessionModel(user_id=user_id, email=email, role=role)
        tokens = cls.jwt_service.create_tokens(user_data=user_session)
        CookieManager.set_jwt_cookies(response, tokens)

        return APIResponse(
            message="Token refreshed successfully",
            data={"access_token": tokens["access_token"]},
        )

    @classmethod
    async def get_user_info(cls, user_id: str, session: AsyncSession):
        existing_user = await UserHelper.get_user_by_id(user_id, session)
        if not existing_user:
            raise UnprocessableEntity(f"User does not exist")

        query = select(User).where(User.id == user_id)
        result = await session.exec(query)
        user = result.first()
        return user
