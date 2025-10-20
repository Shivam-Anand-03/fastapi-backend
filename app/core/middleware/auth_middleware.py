from fastapi import Request
from pydantic import ValidationError
from ...common.services.jwt_services import JwtServices
from ...common.schemas import SessionModel, AuthenticatedUser
from ...common.exceptions import UnauthorizedException
from ...common.settings import settings


class AuthMiddleware:
    def __init__(self, jwt_service: JwtServices):
        self.jwt_service = jwt_service

    async def require_auth(self, request: Request) -> SessionModel:
        token = self._extract_token(request)
        payload = self.jwt_service.decode_token(token, token_type="access")

        try:
            session_data = SessionModel(**payload)
        except (TypeError, ValidationError):
            raise UnauthorizedException("Unauthorized! Invalid or expired token.")

        request.state.user = session_data
        return session_data

    def _extract_token(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]

        token = request.cookies.get("access_token")
        if not token:
            raise UnauthorizedException("Access denied. No token provided.")
        return token


def get_current_user(request: Request) -> AuthenticatedUser:
    user = getattr(request.state, "user", None)
    if not user:
        raise UnauthorizedException(detail="User not authenticated")
    return AuthenticatedUser(user_id=str(user.id), email=user.email)


jwt_service = JwtServices(
    settings.ACCESS_TOKEN_SECRET_KEY, settings.REFRESH_TOKEN_SECRET_KEY
)
auth_middleware = AuthMiddleware(jwt_service=jwt_service)


async def authenticate_user(request: Request) -> AuthenticatedUser:
    await auth_middleware.require_auth(request)
    return get_current_user(request)
