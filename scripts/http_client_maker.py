import inspect

import typing
from fastapi.routing import APIRoute
from typing import get_type_hints

from project_name.app import app
import pydantic

class SignalFuncInfo(object):
    def __init__(self, func):
        self.f = func

    @property
    def origin_code(self) -> str:
        return inspect.getsource(self.f)


def get_object_code(obj) -> str:
    return inspect.getsource(obj)


def get_default_kwargs(func) -> typing.Dict[str, typing.Any]:
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_name(typ) -> str:
    if hasattr(typ, "__name__"):
        return typ.__name__
    return str(typ)


def get_help_info(func) -> str:
    return func.__doc__


def client_func(func) -> str:
    kwargs = []
    default_values = get_default_kwargs(func)
    for k, t in get_type_hints(func).items():
        kwarg = f"{k}:{get_name(t)}"
        if k in default_values:
            kwarg = f"{kwarg} = {default_values[k]}"
        kwargs.append(kwarg)
    # default_values =
    kwargs = [f"{k}:{get_name(v)}" for k, v in get_type_hints(func).items()]
    help_info = get_help_info(func)
    return f"def {func.__name__}()"


T = typing.TypeVar("T")


class NewTyp(typing.Generic[T], pydantic.BaseModel):
    val: T


if __name__ == "__main__":
    app.openapi()
    for route in app.routes:
        if isinstance(route, APIRoute):
            sig = inspect.signature(route.endpoint)
            print(sig.parameters)
            # instance = SignalFuncInfo(route.endpoint)
            # print(instance.origin_code)
