import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel

from src.config.settings import Settings

app = FastAPI()

# Define your email configuration
SMTP_SERVER = Settings().SMTP_HOST
SMTP_PORT = Settings().SMTP_PORT
SMTP_USERNAME = Settings().SMTP_USERNAME
SMTP_PASSWORD = Settings().SMTP_PASSWORD
SENDER_EMAIL = "noreply@ReacruitEase.com"
SENDER_NAME = "RecruitEase"

# Pydantic model for the email request body
class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

# Function to send email using smtplib
def send_email(email: str, subject: str, message: str):
    try:
        # Create the email headers
        msg = MIMEMultipart()
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = email
        msg["Subject"] = subject

        # Attach the email body
        msg.attach(MIMEText(message, "html"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")



