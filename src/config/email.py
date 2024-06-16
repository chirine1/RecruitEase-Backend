from pathlib import Path
from fastapi_mail import (
    FastMail,
    MessageSchema,
    MessageType,
    ConnectionConfig,
)
from fastapi.background import BackgroundTasks

from ..config import Settings

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG

conf = ConnectionConfig(
    MAIL_USERNAME=Settings().SMTP_USERNAME,
    MAIL_PASSWORD=Settings().SMTP_PASSWORD,
    MAIL_PORT=Settings().SMTP_PORT,
    MAIL_SERVER=Settings().SMTP_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_DEBUG=True,
    MAIL_FROM="noreply@RecruitEase.com",
    MAIL_FROM_NAME="Rec APP",
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    USE_CREDENTIALS=True
)


async def send_email(
    recipients: list,
    subject: str,
    context: dict,
    template_name: str,
    background_tasks: BackgroundTasks,
):
    fm = FastMail(conf)

    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html,
    )

    logging.debug("Sending email to recipients: %s", recipients)  # Log recipients
    try:
        background_tasks.add_task(
            fm.send_message,
            message,
            template_name=template_name,
        )
        logging.debug("Email sent successfully.")  # Log successful sending
    except Exception as e:
        logging.error("Error sending email: %s", str(e))  # Log error if sending fails
