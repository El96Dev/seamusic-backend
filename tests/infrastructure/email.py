import pytest

from src.infrastructure.email import HTMLPage, Templater, TemplateSyntaxError


class TestTemplater:
    @pytest.fixture(scope="function")
    def html_template(self) -> HTMLPage:
        return HTMLPage("<html><p>{{param1}}</p><p>{{param2}}</p></html>")

    async def test_templater(self, html_template: HTMLPage) -> None:
        async with Templater() as templater:
            response = await templater.parse(html_page=html_template, param1="value1", param2="value2")

        assert isinstance(response, HTMLPage)
        assert response == HTMLPage("<html><p>value1</p><p>value2</p></html>")

        with pytest.raises(TemplateSyntaxError):
            async with Templater() as templater:
                await templater.parse(html_page=HTMLPage("<html>{{param1</html"), param1="value1", param2="value2")


class TestSMTPSessionMixin:
    async def test_send_email(self, message: HTMLPage, recipient: str, subject: str) -> None:
        ...
