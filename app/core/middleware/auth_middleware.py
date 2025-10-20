from fastapi import Request, HTTPException
from pydantic import ValidationError
from ...common.services.jwt_services import JwtServices
from ...modules.user.user_helper import UserHelper
from ...core.database import DatabaseConnect
from ...schemas import SessionModel


class AuthMiddleware:
    def __init__(self, jwt_service: JwtServices):
        self.jwt_service = jwt_service

    async def require_auth(self, request: Request):
        token: str | None = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            token = request.cookies.get("access_token")

        if not token:
            raise HTTPException(
                status_code=401, detail="Access denied. No token provided."
            )

        payload = self.jwt_service.decode_token(token, token_type="access")

        try:
            session_data = SessionModel(**payload)
        except (TypeError, ValidationError):
            raise HTTPException(
                status_code=401, detail="Unauthorized! Invalid or expired token."
            )

        async with DatabaseConnect.get_session() as session:
            user = await UserHelper.get_user_by_email(session_data.email, session)
            if not user:
                raise HTTPException(
                    status_code=401, detail="User not found. Please log in again."
                )

        request.state.user = user
        return user
