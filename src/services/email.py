from fastapi import BackgroundTasks
from src.config import send_email, Settings
from src.security import Hasher
from src.models import User
from src.utils.helpers import gen_token


async def send_account_verification_email(
    user: User, background_tasks: BackgroundTasks
):
    token = gen_token()
    activate_url = f"{Settings().FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}"
    data = {
        "app_name": Settings().APP_NAME,
        "name": user.fullname,
        "activate_url": activate_url,
    }
    await send_email(
        recipients=[user.email],
        subject=f"Account Verification - {Settings().APP_NAME}",
        template_name="user/account-verification.html",
        context=data,
        background_tasks=background_tasks,
    )


async def send_account_activation_confirmation_email(
    user: User, background_tasks: BackgroundTasks
):
    data = {
        "app_name": Settings().APP_NAME,
        "name": user.fullname,
        "login_url": f"{Settings().FRONTEND_HOST}",
    }
    subject = f"Welcome - {Settings().APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks,
    )


async def send_password_reset_email(
    user: User, background_tasks: BackgroundTasks
):
    token = gen_token()
    reset_url = f"{Settings.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"
    data = {
        "app_name": Settings.APP_NAME,
        "name": user.name,
        "activate_url": reset_url,
    }
    subject = f"Reset Password - {Settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/password-reset.html",
        context=data,
        background_tasks=background_tasks,
    )
