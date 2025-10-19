from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    message: str
    data: T
