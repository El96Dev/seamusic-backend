from dataclasses import dataclass

from src.domain.auth.auth.interfaces.base import BaseInterface


@dataclass
class BaseEmailClient(BaseInterface):
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

    async def send_email(self, template, **params) -> None:
        """
        :param template:
        :param params:
        :raise NotImplementedError:
        :raise SMTPConnectionError:
        """
        raise NotImplementedError
