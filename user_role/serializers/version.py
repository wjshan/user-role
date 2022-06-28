from pydantic import BaseModel
from pydantic import Field


class VersionReturnSerializer(BaseModel):
    version: str = Field(description="版本号")
