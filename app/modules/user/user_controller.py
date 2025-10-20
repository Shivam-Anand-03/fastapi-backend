from app.common.exceptions.base import UnprocessableEntity
from app.common.handlers import APIResponse
from app.modules.user.user_models import User
from app.modules.user.user_helper import UserHelper
from sqlmodel.ext.asyncio.session import AsyncSession


class UserController:
    @classmethod
    async def signup_user_handler(cls, payload, session: AsyncSession):
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
