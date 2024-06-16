from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )


class GenericResponse(BaseModel):
    message: Optional[str] = None
    error: Optional[str] = None
