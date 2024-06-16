from typing import Union, Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr, BaseModel







from .base import BaseResponse


class LoginResponse(BaseResponse):
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    userId: Optional[int] = None
    role: Optional[str] = None
    status: Optional[int] = None
    error: Optional[str] = None

    def __repr__(self):
        return str(self.__dict__)
    
class Token(BaseResponse):
    token: Optional[str]
    #refresh_token: Optional[str]
