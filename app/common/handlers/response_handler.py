from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None

    class Config:
        exclude_none = True
