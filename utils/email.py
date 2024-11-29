from aiosmtplib import SMTP
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

async def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = os.getenv("MAIL_FROM")
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    smtp = SMTP(
        hostname=os.getenv("MAIL_SERVER"),
        port=os.getenv("MAIL_PORT"),
        username=os.getenv("MAIL_USERNAME"),
        password=os.getenv("MAIL_PASSWORD"),
    )

    await smtp.connect()
    await smtp.send_message(msg)
    await smtp.quit()
