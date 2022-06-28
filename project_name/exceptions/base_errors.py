import dataclasses
import traceback
import typing

from typing_extensions import TypedDict

Loc = typing.Tuple[typing.Union[int, str], ...]


class _ErrorDictRequired(TypedDict):
    loc: Loc
    msg: str
    type: str


class ErrorDict(_ErrorDictRequired, total=False):
    ctx: typing.Dict[str, typing.Any]


if typing.TYPE_CHECKING:
    from fastapi.exceptions import ValidationError as V

    # from pydantic.error_wrappers import ErrorDict

T = typing.TypeVar("T")

NoneType = type(None)


@dataclasses.dataclass
class BaseError(Exception):
    status_code: int = 500
    code: int = 500
    message: str = "未知错误"
    data: type(None) = None

    @property
    def detail(self):
        from project_name.config import settings
        return traceback.format_exc(limit=5) if settings.server.debug else None

    def json(self):
        return {"code": self.code, "message": self.message, "detail": self.detail, "data": self.data}

    @classmethod
    def to_response_obj(cls):
        """返回当前模型的response个格式"""
        return {cls.status_code: {"model": cls}}


@dataclasses.dataclass
class UrlNotFindError(BaseError):
    code: int = 404
    status_code: int = 404
    message: str = "Url Not Found"


@dataclasses.dataclass
class ResourceNotFoundError(BaseError):
    code: int = 4040
    status_code: int = 404
    message: str = "Resource Not Found"


@dataclasses.dataclass
class ValidateError(BaseError):
    code: int = 422
    status_code: int = 422
    message: str = "参数校验错误"
    data: typing.List[ErrorDict] = dataclasses.field(default_factory=list)

    @classmethod
    def convert_fastapi_error(cls, e: "V"):
        return cls(data=e.errors())
