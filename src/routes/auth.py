from datetime import datetime, timedelta
from typing import Annotated, List

from fastapi import  BackgroundTasks, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse




from src.controllers import auth_controller
from src.services.email_smtplib import send_account_verification_email
from src.utils.email import EmailSchema, send_email
from src.controllers.auth_controller import AuthController
from src.payload import LoginResponse
from src.payload.requests.auth import Email, LoginBody

from src.payload.responses.base import GenericResponse
from src.schemas.activation_code import ActivationCodeVerify
from src.schemas.user import ResetPassword, ResetPasswordAccount, User, UserOut 
from src.schemas.user import UserCreate
from src.security.access_token_bearer2 import AccessTokenBearer2
from src.security.refresh_token_bearer import RefreshTokenBearer

from src.utils.helpers import generate_code
from .routers import auth_router



@auth_router.post("/login")
async def login(
    body: LoginBody,
    auth_controller: Annotated[AuthController, Depends()],
    response: Response,
):
    resp = await auth_controller.authenticate_user(body,response)


    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="Invalid credentials!"
            ).__dict__,
        )

    return resp

@auth_router.get("/refresh", )
async def refresh_token(
    auth_controller: Annotated[AuthController, Depends()],
    request: Request,
    response: Response
):
    return await auth_controller.refresh_token(request,response)

@auth_router.post("/signup", response_model=GenericResponse)
async def signup(
    body: UserCreate,
    auth_controller: Annotated[AuthController, Depends()],
):
    return await auth_controller.register_user(body)


@auth_router.get("",response_model=List[User])
async def get_all_users(
    auth_controller: Annotated[AuthController, Depends()]
):
    return await auth_controller.get_all()


@auth_router.delete("/logout")
async def logout(
):
    response = JSONResponse(
        status_code=200,
        content={
            "message": "Successfully logged out",
            "error": None
        }
    )
    response.delete_cookie(key="access_token", path="/", httponly=True , domain="localhost")
    response.delete_cookie(key="refresh_token", path="/", httponly=True , domain="localhost")
    return response

@auth_router.get("/current",response_model=UserOut)
async def get_current_user(
    auth_controller: Annotated[AuthController, Depends()],
    token: str = Depends(AccessTokenBearer2())
):
    resp = await auth_controller.get_current_user(token)
    if not resp:
        raise HTTPException(
            status_code=404,
            detail="did not find user, log in again"
        )
    return resp


@auth_router.get("/{id}",response_model=UserOut)
async def get_user_by_id(
    auth_controller: Annotated[AuthController, Depends()],
    id:int
):
    resp = await auth_controller.get_user_by_id(id)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="This use does not exist"
            ).__dict__,
        )
    return resp
 
@auth_router.get("/user/curent",response_model=int)
async def get_current_user_id(
    auth_controller: Annotated[AuthController, Depends()],
    token: str = Depends(AccessTokenBearer2())
):
    return await auth_controller.get_current_user_id(token)

 


@auth_router.post("/send_email")
async def send_email_route( body: Email , background_tasks: BackgroundTasks):
    email_data = EmailSchema(
        email=body.email,
        subject= "activation",
        message="please use this code : Hy62Tm"
    )
    background_tasks.add_task(send_email, email_data.email, email_data.subject, email_data.message)
    return {"message": "Email sending in progress"}

@auth_router.post("/verify_code")
async def verify_code(
    body : ActivationCodeVerify,
    auth_controller: Annotated[AuthController, Depends()],
):
   return await auth_controller.confirm_email(body)

@auth_router.post("/forgot_password_mail")
async def forgot_password( body: Email , background_tasks: BackgroundTasks):
    email_data = EmailSchema(
        email=body.email,
        subject= "forgot password",
        message="please use this code : Si98Df"
    )
    background_tasks.add_task(send_email, email_data.email, email_data.subject, email_data.message)
    return {"message": "Email sending in progress"}

@auth_router.post("/verify_reset_code")
async def verify_reset_code(
    body : ActivationCodeVerify,
    auth_controller: Annotated[AuthController, Depends()],
):
   return await auth_controller.verify_reset_code(body)


@auth_router.post("/reset_password")
async def reset_password(
    body: ResetPassword,
    auth_controller: Annotated[AuthController, Depends()],
):
    return await auth_controller.reset_password(body)

@auth_router.post("/reset_password_account")
async def reset_password_account(
    body: ResetPasswordAccount,
    auth_controller: Annotated[AuthController, Depends()],
    token: str = Depends(AccessTokenBearer2())
):
    return await auth_controller.reset_password_account(body,token)

@auth_router.put("/ban_user/{id}")
async def ban_user(
    id: int,  
    auth_controller: Annotated[AuthController, Depends()],
):
    resp = await auth_controller.ban_user(id)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="This user does not exist"
            ).__dict__,
        )
    return resp