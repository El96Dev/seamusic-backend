from dataclasses import dataclass
from types import TracebackType
from typing import Self

from src.domain.auth.auth.interfaces.base import BaseInterface


@dataclass
class EmailClient(BaseInterface):
    """
    BaseEmailClient is an abstract class created to define
    and describe necessary functions for email client.

    It's used in services' layer to send and manage emails.

    As an abstraction, BaseEmailClient cannot be used directly -
    that will cause `NotImplementedError` and crash the application.
    So, to provide the email management, a BaseEmailClient
    implementation is required.

    BaseEmailClient implementation is a DAO's subclass designed in a
    unique way for an exact type of storage. It can ONLY be used for
    email management with data in that type of storage. The implementation
    must be provided to the service's layer via factory to avoid using
    globals.
    """

    async def send_email(
        self,
        recipient: str,
        template_path: str,
        **params: dict,
    ) -> None:
        """
        :param recipient: email adress of an email receiver
        :param template_path: HTML-template (taken from presentation layer)
          full path & name & extension
        :param params: parameters to insert into template
        :raise SMTPConnectionError: when there is a problem with connection
          beetwen the app and
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ) -> None:
        pass
