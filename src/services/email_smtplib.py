

from fastapi import BackgroundTasks


from src.utils.email import send_email


async def send_account_verification_email(email: str, code: str):
    subject = "Account Verification - RecruitEase"
    message = f"activation code : {code}"
    send_email(email, subject, message)
    return {"message": "Verification email sent"}