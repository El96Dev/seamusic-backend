from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from types import TracebackType
from typing import Any, Self

import aiosmtplib

from src.infrastructure.config import settings


class TemplateSyntaxError(SyntaxError):
    """Syntax problem in HTML template"""


class HTMLPage(str):
    """HTML email template type"""


class Templater:
    params: dict[str, Any]

    def replace(self, string_part: str) -> str:
        """
        Auxiliary method for replacing parameter's placeholder with
        parameter's value

        :param string_part: part of a page after "{{"
        :return str: same part, but parameter's value is filled
          and ""{{"" & "}}" are removed
        :raise IndexError: when brackets are used incorrectly
        """

        part: list[str] = string_part.split('}}')
        param: str = part[0]
        right: str = part[1]
        return f"{self.params.get(param, '')}{right}"

    async def parse(self, html_page: HTMLPage, **params) -> HTMLPage:  # type: ignore[no-untyped-def]
        """
        Main method that fills parameters' values into template page

        :param html_page: text of an HTML template
        :param params: parameters to fill
        :return HTMLPage: ready-to-render HTML page with filled params
        """

        self.params: dict[str, Any] = params
        page: list[str] = html_page.split("{{")
        return HTMLPage(str(page[0]) + str().join(list(map(self.replace, page[1:]))))

    async def __aenter__(self) -> Self:
        """
        :return Self: instance returns itself when entering an
          asynchronous context manager
        """

        return self

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Closes the asynchronous context manager, handles occured exceptions
        and transforms them into developer-friendly ones

        :param exc_type: exception class
        :param exc_val: exception instance
        :param exc_tb: full traceback
        :raise TemplateSyntaxError: when brackets are used incorrectly
        """
        if exc_type == IndexError:
            raise TemplateSyntaxError("Brackets are used incorrectly")


@dataclass
class SMTPSessionMixin:
    """
    SMTPSessionMixin is a mixin class for email interface implementation
    that should be used via an asynchronous context manager
    """

    @staticmethod
    async def send_email(message: HTMLPage, recipient: str, subject: str) -> None:
        """

        :param message:
        :param recipient:
        :param subject:
        :return:
        """

        sender = settings.email_address
        password = settings.email_password

        smtp_host = settings.smtp_host
        smtp_port = settings.smtp_port

        server = aiosmtplib.SMTP(hostname=smtp_host, port=smtp_port)
        await server.starttls()
        await server.login(sender, password)

        msg = MIMEMultipart()
        msg["From"], msg["To"], msg["Subject"] = sender, recipient, subject

        msg.attach(MIMEText(message, "plain", "utf-8"))

        await server.sendmail(sender, recipient, msg.as_string())
