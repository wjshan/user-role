from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Any, TypeVar, Generic

T = TypeVar("T")


class BaseResponseSerializer(GenericModel, Generic[T]):
    code: int = 0
    message: str = None
    detail: str = None
    data: T = None
