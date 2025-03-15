from typing import Iterator

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from src.app.auth.auth.interfaces.email.client import EmailClientImplementation


class TestEmailClientImplementation:
    @pytest.fixture
    def email_client() -> Iterator[EmailClientImplementation]:
        client = EmailClientImplementation()
        with patch("aiosmtplib.SMTP", new_callable=AsyncMock) as mock_smtp:
            mock_server = mock_smtp.return_value
            mock_server.sendmail.return_value = None
            yield client

    @pytest.mark.asyncio
    async def test_send_email(email_client):
        with pytest.raises(None):
            template_path = (
                Path(__file__).parent
                / "../../../../src/presentation/templates/letter.html"
            )
            await email_client.send_email(
                recipient="test@example.com",
                subject="Test Subject",
                template_path=template_path,
                confirm_url="https://example.com/confirm"
            )

    @pytest.mark.asyncio
    async def test_html_parsing(email_client):
        html_template = '<a href="{{confirm_url}}">{{confirm_url}}</a>'
        html_expected = '<a href="https://example.com/confirm">' \
                        'https://example.com/confirm</a>'
        message = email_client.parse(
            html_template,
            {"confirm_url": "https://example.com/confirm"}
        )

        assert message == html_expected

    @pytest.mark.asyncio
    async def test_incorrect_html_template_syntax(email_client):
        html_template = '<a href="{{confirm_url">{{confirm_url</a>'
        with pytest.raises(IndexError):
            email_client.parse(
                html_template,
                {"confirm_url": "https://example.com/confirm"}
            )

    @pytest.mark.asyncio
    async def test_send_email_file_not_found(email_client):
        with pytest.raises(FileNotFoundError):
            await email_client.send_email(
                recipient="test@example.com",
                subject="Test Subject",
                template_path="nonexistent_template.html",
                confirm_url="https://example.com/confirm"
            )
