from fastapi import Response
from typing import Dict


class CookieManager:
    @staticmethod
    def set_jwt_cookies(response: Response, tokens: Dict[str, str]):

        response.set_cookie(
            key="access_token",
            value=tokens.get("access_token"),
            httponly=True,
            max_age=15 * 60,
            expires=15 * 60,
            samesite="lax",
            secure=False,
        )

        # Refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=tokens.get("refresh_token"),
            httponly=True,
            max_age=7 * 24 * 60 * 60,
            expires=7 * 24 * 60 * 60,
            samesite="lax",
            secure=False,
        )
