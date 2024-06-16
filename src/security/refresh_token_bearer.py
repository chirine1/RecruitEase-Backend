from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from src.payload.responses import GenericResponse
from .jwt_manager import JwtManager


class RefreshTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(RefreshTokenBearer, self).__init__(
            auto_error=auto_error
        )

    async def __call__(self, request: Request):
        credentials: Optional[
            HTTPAuthorizationCredentials
        ] = await super(RefreshTokenBearer, self).__call__(
            request
        )

        if not credentials:
            raise HTTPException(status_code=403)

        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=401,
                detail=GenericResponse(
                    error="Invalid token!", message=None
                ).__dict__,
            )

        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(
                status_code=401,
                detail=GenericResponse(
                    error="Expired token!", message=None
                ).__dict__,
            )

        return credentials.credentials

    def verify_jwt(self, token: str) -> bool:

        return JwtManager.check_token_validity(
            JwtManager.decode_refresh(token)["exp"]
        )
