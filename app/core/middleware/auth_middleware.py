from fastapi import Request
from pydantic import ValidationError
from ...common.services.jwt_services import JwtServices
from ...common.schemas import SessionModel, AuthenticatedUser
from ...common.exceptions import (
    UnauthorizedException,
    TokenExpiredException,
    TokenNotPresentException,
)
from ...common.settings import settings


class AuthMiddleware:
    def __init__(self, jwt_service: JwtServices):
        self.jwt_service = jwt_service

    async def require_auth(self, request: Request) -> SessionModel:
        access_token = request.cookies.get("access_token") or self._extract_token(
            request, "access"
        )
        refresh_token = request.cookies.get("refresh_token") or self._extract_token(
            request, "refresh"
        )

        if not access_token or not refresh_token:
            raise TokenNotPresentException("Access or Refresh token not provided.")

        access_result = self.jwt_service.decode_token(access_token, token_type="access")
        if access_result["is_expired"]:
            raise TokenExpiredException(
                "Access token expired. Please refresh your session."
            )

        refresh_result = self.jwt_service.decode_token(
            refresh_token, token_type="refresh"
        )

        if refresh_result["is_expired"]:
            raise TokenNotPresentException("Refresh token is invalid.")

        try:
            session_data = SessionModel(**access_result["payload"])
        except (TypeError, ValidationError):
            raise UnauthorizedException("Unauthorized! Invalid token data.")

        request.state.user = session_data
        return session_data

    def _extract_token(
        self, request: Request, token_type: str = "access"
    ) -> str | None:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None


def get_current_user(request: Request) -> AuthenticatedUser:
    user = getattr(request.state, "user", None)
    if not user:
        raise UnauthorizedException("User not authenticated")
    return AuthenticatedUser(user_id=str(user.user_id), email=user.email)


jwt_service = JwtServices(
    settings.ACCESS_TOKEN_SECRET_KEY, settings.REFRESH_TOKEN_SECRET_KEY
)
auth_middleware = AuthMiddleware(jwt_service=jwt_service)


async def authenticate_user(request: Request) -> AuthenticatedUser:
    await auth_middleware.require_auth(request)
    return get_current_user(request)
