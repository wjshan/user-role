import inspect
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    Union, get_origin,
)

from fastapi import params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.routing import APIRoute
from fastapi.utils import (
    generate_unique_id,
)
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.routing import Mount as Mount  # noqa
from user_role.serializers.public_serializer import BaseResponseSerializer
from .docstrings import convert

class BaseResponseSerializer2(BaseResponseSerializer):
    pass

class CustomRoute(APIRoute):
    """
    自动将返回格式包装为标准格式
    """

    def __init__(
            self,
            path: str,
            endpoint: Callable[..., Any],
            *,
            response_model: Optional[Type[Any]] = None,
            status_code: Optional[int] = None,
            tags: Optional[List[Union[str, Enum]]] = None,
            dependencies: Optional[Sequence[params.Depends]] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            deprecated: Optional[bool] = None,
            name: Optional[str] = None,
            methods: Optional[Union[Set[str], List[str]]] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Union[Type[Response], DefaultPlaceholder] = Default(
                JSONResponse
            ),
            dependency_overrides_provider: Optional[Any] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Union[
                Callable[["APIRoute"], str], DefaultPlaceholder
            ] = Default(generate_unique_id),
    ) -> None:
        get_origin(response_model)
        if response_model is None:
            sig = inspect.signature(endpoint)
            if sig.return_annotation is not sig.empty:
                response_model = BaseResponseSerializer[sig.return_annotation]
        elif not issubclass(response_model,BaseResponseSerializer):
            response_model = BaseResponseSerializer[response_model]
        super(CustomRoute, self).__init__(
            path=path, endpoint=endpoint, response_model=response_model, status_code=status_code, tags=tags,
            dependencies=dependencies, summary=summary,
            description=description, response_description=response_description, responses=responses,
            deprecated=deprecated, name=name, methods=methods, operation_id=operation_id,
            response_model_include=response_model_include, response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            dependency_overrides_provider=dependency_overrides_provider,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )
