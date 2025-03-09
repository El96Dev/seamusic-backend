import pytest
from fastapi import HTTPException, status

from src.infrastructure.api import ExceptionHandler
from src.infrastructure.exceptions import Exc


class TestExceptionHandler:
    @pytest.fixture(scope="function")
    def exceptions(self) -> dict[type[Exc], HTTPException]:
        return {Exc: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="detail")}

    async def test_exception_handler(self, exceptions: dict[type[Exc], HTTPException]) -> None:
        with pytest.raises(HTTPException):
            async with ExceptionHandler(exceptions=exceptions):
                raise Exc()
