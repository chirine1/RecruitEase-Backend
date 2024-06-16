from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import BackgroundTasks, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse


from src.models.candidate import Candidate
from src.models.company import Company
from src.models.user import ActivationCode, User
from src.payload.requests.auth import LoginBody
from src.payload.responses.auth import LoginResponse, Token
from src.payload.responses.base import GenericResponse
from src.schemas.activation_code import ActivationCodeVerify
from src.schemas.user import ResetPassword, ResetPasswordAccount, UserCreate
from src.security.access_token_bearer2 import AccessTokenBearer2
from src.security.hasher import Hasher
from src.security.jwt_manager import JwtManager
from src.security.refresh_token_bearer import RefreshTokenBearer
from src.services.candidate import CandidateService
from src.services.company import CompanyService
from src.services.email_smtplib import send_account_verification_email
from src.services.user import AuthService
from random import randint as rdn

from src.utils.helpers import generate_code



class AuthController:

    def __init__(
        self,
        auth_service: Annotated[AuthService, Depends()],
        candidate_service: Annotated[CandidateService, Depends()],
        company_service: Annotated[CompanyService, Depends()],
    ) -> None:
        self.auth_service = auth_service
        self.candidate_service = candidate_service
        self.company_service = company_service

    async def authenticate_user(
        self,
        body: LoginBody,
        response: Response
    ) :
        user: Optional[User] = (
            await self.auth_service.find_user_by_email(
                body.email
            )
        )

        if not user:
            return
      
        if not Hasher.verify_hash(
            body.password, (getattr(user,"hashed_password"))
        ):
            return
       
        if not getattr(user,"status") == 1:         #activation
            return   JSONResponse(
                    status_code=401,
                    content=GenericResponse(
                        error=f"not activated", message="account not activated please verify account"
                    ).__dict__,
                )
        
        if not user.ban_status == "active":
            return    JSONResponse(
                    status_code=409,
                    content=GenericResponse(
                        error=f"account banned", message="your account has been banned"
                    ).__dict__,
                )
        
        access_token=JwtManager.create_access_token(sub=str(user.id))
        ref_token = JwtManager.create_refresh_token(sub=f"{rdn(1000, 9999) * 17}")

        response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800000,
        expires=1800000,
        )
        response.set_cookie(
        key="refresh_token",
        value=f"Bearer {ref_token}",
        httponly=True,
        max_age=60480000,
        expires=60480000,
        )
        
        return LoginResponse(
            token = access_token,
            refresh_token=ref_token,
            userId=user.id, 
            role=user.role,
            status=getattr(user,"status"),
        )
    

    async def register_user(self, body: UserCreate):
        user: Optional[User] = (await self.auth_service.find_user_by_email(body.email))
        
        if user:
            return JSONResponse(
                status_code=400,
                content=GenericResponse(
                    error="Account already exists!",
                    message=None,
                ).__dict__,
            )

        else:
            try:
                user = User(
                    fullname=body.fullname,
                    email=body.email,
                    hashed_password=Hasher.hash_text(
                        body.password
                    ),
                    status=0,
                    role = body.role,
                )
               
                code = ActivationCode(
                    email=body.email,
                    code=generate_code(),
                    expires_at=datetime.now()
                    + timedelta(minutes=15),
                    user=user,
                )
                await self.auth_service.insert_user(user)
                await self.auth_service.insert_code(code)
                
                #get the new user with its new id
                user: Optional[User] = (await self.auth_service.find_user_by_email(body.email))
                #now create secondary object 
                if user:
                    id = user.id

                    
                if body.role == "candidate":
                    await self.candidate_service.create(id)
                     

                if body.role == "recruiter":
                    await self.company_service.create(id)

            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content=GenericResponse(
                        error=f"{e}", message="something went wrong"
                    ).__dict__,
                )
            
      
            
            return GenericResponse(
                message="Account creation success!",
                error=None,
            )
       

    async def get_all(self):
        return  await self.auth_service.get_all()
    
    async def get_user_by_id(self,id:int) -> Optional[User]:
        return await self.auth_service.get_one(id)


    async def refresh_token(
        self,
        request: Request,
        response: Response
        ):
        refresh_token  = request.cookies.get("refresh_token")
        if not refresh_token:
            return HTTPException(status_code=401, detail="Refresh token not found")
        
        if not refresh_token.startswith("Bearer "):
            return  HTTPException(
                status_code=401,
                detail=GenericResponse(
                    error="Invalid token format!", message=None
                    ).__dict__,
                )
    
        # Strip 'Bearer ' prefix
        refresh_token = refresh_token[len("Bearer "):]
        
        if not JwtManager.check_token_validity(
            JwtManager.decode_refresh(refresh_token)["exp"]
        ):
            return HTTPException(
                status_code=401,
                detail=GenericResponse(
                    error="Expired token!", message=None
                ).__dict__,
            )
      
        
        payload = JwtManager.decode_refresh(refresh_token)
        id: str = payload.get("sub") # type: ignore
    
        access_token = JwtManager.create_access_token(id)
        response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=18000,
        expires=18000,
        )

        return Token(
            token= access_token,
        )


    async def get_current_user_id(
        self,
        token: str 
    ) :
        # No need to check if token is present, AccessTokenBearer handles it

        payload = JwtManager.decode_access(token)
        user_id: int = int(payload.get("sub")) # type: ignore
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        """ user: Optional[User] = await AuthService.get_one(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found") """
        
        print(f"\n\n user id is : {user_id}\n\n")
        
        return user_id
    

    async def confirm_email(
            self,
            body: ActivationCodeVerify,
    ):        
        user: Optional[User] = await self.auth_service.find_user_by_email(body.email)

        if not user:
            return HTTPException(
                status_code=404,
                detail=GenericResponse(
                    error="wrong email!", message=None
                ).__dict__,
            )
        if body.code == "Hy62Tm":
            await self.auth_service.activate_user(user.id)
            return GenericResponse(
                message="code correct your account is verified",
                error=None
                )
        return GenericResponse(
            message="code is wrong ",
            error="verification code is wrong for this email"
            )
    
    async def send_verification_email(
        self,
        email: str,
        background_tasks: BackgroundTasks ,
    ):
        user = await self.auth_service.find_user_by_email(email)
        code = ActivationCode(
                        email=email,
                        code=generate_code(),
                        expires_at=datetime.now()
                        + timedelta(minutes=15),
                        user=user,
                    )
        await self.auth_service.insert_code(code)
        
        background_tasks.add_task(send_account_verification_email, email, "666666")
        return {"message": "Email sent successfully"}
    

    async def verify_reset_code(self,body: ActivationCodeVerify):
        if body.code == "Si98Df" :
            return JSONResponse(
                status_code=200,
                content = "code correct!"
            )
        return  JSONResponse(
                status_code=401,
                content = "wrong code"
            )
    
    async def reset_password(self,body: ResetPassword):
        resp = await self.auth_service.reset_password(body)

        if not resp: 
            JSONResponse(
                status_code=404,
                content=GenericResponse(
                    error="wrong email!", message=None
                ).__dict__,
            )

        return JSONResponse(
            status_code=200,
            content="password changed succesfully"
        )
    
    async def reset_password_account(self, body: ResetPasswordAccount, token: str):
        user_id = await self.get_current_user_id(token)
        success = await self.auth_service.reset_password_account(body, user_id)
        print(f"token: {token} id : {user_id}")
        if not success:
            return JSONResponse(
                status_code=404,
                content=GenericResponse(
                    error="Wrong email or password",
                    message=None
                ).dict(),
            )
                
        return JSONResponse(
            status_code=200,
            content={"message": "Password changed successfully"}
        )

    async def ban_user(self,user_id):
        return await self.auth_service.ban_user(user_id)
    

    async def create_admin(self):
        return await self.auth_service.insert_user(
                User(
                    fullname="admin",
                    email="admin@recruitease.com",
                    hashed_password=Hasher.hash_text(
                        "admin123"
                    ),
                    status=1,
                    role = "admin",
                    ban_status = "active",
                )
        )

    async def get_current_user(self,token):
        id = await self.get_current_user_id(token)
        return await self.auth_service.get_one(id)
    
