from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from src.infrastructure.config import settings


@dataclass
class SMTPSessionMixin:
    @staticmethod
    async def send_email(message: str, recipient: str, subject: str) -> None:
        sender = settings.email_address
        password = settings.email_password

        smtp_host = settings.smtp_host
        smtp_port = settings.smtp_port

        server = aiosmtplib.SMTP(hostname=smtp_host, port=smtp_port)
        await server.starttls()
        await server.login(sender, password)

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject

        body = message
        msg.attach(MIMEText(body, "plain", "utf-8"))

        await server.sendmail(sender, recipient, msg.as_string())
