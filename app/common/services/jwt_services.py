from datetime import timedelta
import jwt
from ..utils.datetime import utcnow
from ..schemas import TokenModel


class JwtServices:
    def __init__(self, access_token_secret_key: str, refresh_token_secret_key: str):
        self.access_secret = access_token_secret_key
        self.refresh_secret = refresh_token_secret_key
        self.algorithm = "HS256"

    def create_tokens(
        self,
        user_data: dict,
        access_expiry: timedelta = timedelta(days=1),
        refresh_expiry: timedelta = timedelta(days=7),
    ) -> TokenModel:
        """Create both access and refresh tokens"""
        now = utcnow()

        access_payload = user_data.copy()
        access_payload["exp"] = now + access_expiry
        access_token = jwt.encode(
            access_payload, self.access_secret, algorithm=self.algorithm
        )

        refresh_payload = user_data.copy()
        refresh_payload["exp"] = now + refresh_expiry
        refresh_token = jwt.encode(
            refresh_payload, self.refresh_secret, algorithm=self.algorithm
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def decode_token(self, token: str, token_type: str = "access"):
        """Decode access or refresh token"""
        secret = self.access_secret if token_type == "access" else self.refresh_secret
        try:
            payload = jwt.decode(token, secret, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return f"{token_type.capitalize()} token expired"
        except jwt.InvalidTokenError:
            return f"Invalid {token_type} token"


if __name__ == "__main__":
    jwt_service = JwtServices("access-secret-key", "refresh-secret-key")
    user = {"user_id": 1, "username": "shivam"}

    tokens = jwt_service.create_tokens(user)
    print("Tokens:", tokens)

    print("Decoded Access:", jwt_service.decode_token(tokens["access_token"], "access"))
    print(
        "Decoded Refresh:", jwt_service.decode_token(tokens["refresh_token"], "refresh")
    )
