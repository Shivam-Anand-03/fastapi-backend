from fastapi import Request
from ...common.exceptions import UnauthorizedException
from ...common.schemas import AuthenticatedUser


def get_current_user(request: Request) -> AuthenticatedUser:
    user = getattr(request.state, "user", None)
    if not user:
        raise UnauthorizedException(detail="User not authenticated")

    return AuthenticatedUser(user_id=str(user.id), email=user.email)


async def authenticate_user(request: Request) -> AuthenticatedUser:
    await auth_middleware.require_auth(request)
    return get_current_user(request)
