import io
import os
from typing import (
    Any,
    Optional,
)

from fastapi import FastAPI
from fastapi.exceptions import ValidationError, RequestValidationError
from starlette.background import BackgroundTask
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from project_name.serializers.public_serializer import BaseResponseSerializer
from .config import settings
from .exceptions.base_errors import BaseError, ValidateError, UrlNotFindError
from .routes import main_router


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("VERSION")
    """
    with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


class PublicBaseResponse(JSONResponse):
    def __init__(self, content: Any,
                 status_code: int = 200,
                 headers: Optional[dict] = None,
                 media_type: Optional[str] = None,
                 background: Optional[BackgroundTask] = None, ):
        data = BaseResponseSerializer(data=content)
        super(PublicBaseResponse, self).__init__(dict(data), status_code, headers, media_type, background)


async def error_404(request, exc):
    return JSONResponse(UrlNotFindError().json())


async def base_error_handler(request: Request, exc: BaseError):
    return JSONResponse(exc.json(), status_code=exc.status_code)


async def validation_error_handler(request: Request, exc: ValidationError):
    error = ValidateError.convert_fastapi_error(exc)
    return JSONResponse(error.json(), status_code=error.status_code)


async def unknown_error_handler(request: Request, exc: Exception):
    error = BaseError(message=str(exc))
    return JSONResponse(error.json(), status_code=error.status_code)


app = FastAPI(
    title="project_name",
    description="project_name API helps you do awesome stuff. 🚀",
    version=read("VERSION"),
    terms_of_service="http://project_name.com/terms/",
    # responses={"default": {"model": BaseResponseSerializer}, "200": {"model": BaseResponseSerializer}},
    default_response_class=PublicBaseResponse,
    exception_handlers={
        BaseError: base_error_handler,
        RequestValidationError: validation_error_handler,
        Exception: unknown_error_handler,
        404: error_404
    },
)

if settings.server and settings.server.get("cors_origins", None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(main_router)
