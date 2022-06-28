import io
import os
from typing import Literal

from fastapi import APIRouter

from project_name.exceptions.base_errors import ValidateError
from project_name.serializers.version import VersionReturnSerializer
from project_name.utils.route import CustomRoute

router = APIRouter(route_class=CustomRoute)


@router.get('/version')
def version() -> VersionReturnSerializer:
    """
    # 读取版本号
    """
    with io.open(
            os.path.join(os.path.dirname(__file__), '..', "VERSION"),
            encoding="utf8",
    ) as open_file:
        content = open_file.read().strip()
    return VersionReturnSerializer(version=content)
