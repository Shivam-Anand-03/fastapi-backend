from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType,
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "template"


class MailService:
    def __init__(
        self, mail_username: str, mail_password: str, mail_from: str, mail_server: str
    ):
        self.config = ConnectionConfig(
            MAIL_USERNAME=mail_username,
            MAIL_PASSWORD=mail_password,
            MAIL_FROM=mail_from,
            MAIL_PORT=465,
            MAIL_SERVER=mail_server,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_DIR=TEMPLATE_DIR,
        )

        self.mail = FastMail(self.config)

    async def send_email(self, subject: str, recipients: list[str], body: str):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html,
        )
        await self.mail.send_message(message)
        print("📧 Email sent successfully!")
