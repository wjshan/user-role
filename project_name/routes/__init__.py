from fastapi import APIRouter

from project_name.exceptions.base_errors import UrlNotFindError, ResourceNotFoundError, ValidateError
from .version import router as version_router

main_router = APIRouter(prefix="/api", responses={
    422: {"model": ValidateError},
    404: {"model": UrlNotFindError},
})
main_router.include_router(version_router, tags=["version"])
