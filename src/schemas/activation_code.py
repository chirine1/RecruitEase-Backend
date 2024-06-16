from datetime import datetime, timezone

from typing import Optional
from openai import BaseModel
from pydantic import EmailStr
from sqlalchemy import DateTime, func


from src.schemas.base_schema import OrmSchema 


class ActivationCodeBase(OrmSchema):
    email: str 
    code: str 

    created_at: datetime 

    expires_at: datetime 


class ActivationCodeRead(ActivationCodeBase):
    id_code: int

class ActivationCodeVerify(BaseModel):
    code: str
    email: str