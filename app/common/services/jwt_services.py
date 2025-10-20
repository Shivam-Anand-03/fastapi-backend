from datetime import timedelta
import jwt
from ..utils.datetime import utcnow
from ..schemas import TokenModel, SessionModel
from ...common.exceptions import UnauthorizedException


class JwtServices:
    def __init__(self, access_token_secret_key: str, refresh_token_secret_key: str):
        self.access_secret = access_token_secret_key
        self.refresh_secret = refresh_token_secret_key
        self.algorithm = "HS256"

    def create_tokens(
        self,
        user_data: SessionModel,
        access_expiry: timedelta = timedelta(days=1),
        refresh_expiry: timedelta = timedelta(days=7),
    ) -> TokenModel:
        now = utcnow()

        user_dict = user_data.model_dump()

        access_payload = user_dict.copy()
        access_payload["exp"] = now + access_expiry
        access_token = jwt.encode(
            access_payload, self.access_secret, algorithm=self.algorithm
        )

        refresh_payload = user_dict.copy()
        refresh_payload["exp"] = now + refresh_expiry
        refresh_token = jwt.encode(
            refresh_payload, self.refresh_secret, algorithm=self.algorithm
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def decode_token(self, token: str, token_type: str = "access") -> dict:
        secret = self.access_secret if token_type == "access" else self.refresh_secret
        try:
            payload = jwt.decode(token, secret, algorithms=[self.algorithm])
            return {"payload": payload, "is_expired": False}
        except jwt.ExpiredSignatureError:
            return {"payload": None, "is_expired": True}
        except jwt.InvalidTokenError:
            raise UnauthorizedException(f"Invalid {token_type} token")
