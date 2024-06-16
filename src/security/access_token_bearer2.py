

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import ExpiredSignatureError

from src.payload.responses import GenericResponse

class AccessTokenBearer2(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AccessTokenBearer2, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        # Extract token from the 'access_token' cookie
        token = request.cookies.get("access_token")
        
        if not token:
            raise HTTPException(status_code=403, detail="Not authenticated")

        # Ensure the token uses the 'Bearer' scheme
        if not token.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail=GenericResponse(
                    error="Invalid token!", message=None
                ).__dict__,
            )

        token = token[7:]  # Remove "Bearer " prefix to get the actual token
        
        if not self.verify_jwt(token):
            raise HTTPException(
                status_code=401,
                detail=GenericResponse(
                    error="Expired token!", message=None
                ).__dict__,
            )

        return token

    """ def verify_jwt(self, token: str) -> bool:
        from .jwt_manager import JwtManager
        return JwtManager.check_token_validity(JwtManager.decode_access(token)["exp"]) """
    def verify_jwt(self, token: str) -> bool:
        from .jwt_manager import JwtManager
        try:
            return JwtManager.check_token_validity(JwtManager.decode_access(token)["exp"])
        except ExpiredSignatureError:
            return False
