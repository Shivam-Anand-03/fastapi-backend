from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


class SessionModel(BaseModel):
    user_id: str
    email: str
    role: str


class AuthenticatedUser(SessionModel):
    pass
