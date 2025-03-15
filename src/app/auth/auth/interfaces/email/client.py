from src.domain.auth.auth.interfaces.email.client import EmailClient
from src.infrastructure.email import HTMLPage, SMTPSessionMixin, Templater


class EmailClientImplementation(EmailClient, SMTPSessionMixin, Templater):
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
        subject: str,
        template_path: str,
        confirm_url: str,
    ) -> None:
        """
        :param recipient: email adress of an email receiver
        :param subject: email message subject
        :param template_path: HTML-template (taken from presentation layer)
          full path & name & extension
        :param confirm_url: URL for confirmation of an action
        :raise SMTPConnectionError: when there is a problem with connection
          beetwen the app and
        """

        params = {"confirm_url": confirm_url}
        with open(template_path, 'r', encoding='utf-8') as file:
          html_template = HTMLPage(file.read())

        message = HTMLPage(self.parse(html_template, **params))

        await self.send_smtp_email(message, recipient, subject)
