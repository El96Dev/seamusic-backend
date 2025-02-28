from types import TracebackType

from fastapi import HTTPException
from src.infrastructure.exceptions import Exc


class ExceptionHandler:
    """
    Class for handling exceptions on API level. Usually, the exceptions
    are raised on lower layers, so API-layer has to convert them into
    client-friendly ones
    """

    def __init__(self, exceptions: dict[type[Exc], HTTPException]):
        """
        :param exceptions: dictionary mapping low-level exception types to client-friendly ones
        """
        self.exceptions = exceptions

    async def __aenter__(self) -> "ExceptionHandler":
        return self

    async def __aexit__(self, exc_type: type[Exc] | None, exc_val: Exc | None, exc_tb: TracebackType | None) -> None:
        if exc_type and exc_val and (translated_exc := self.exceptions.get(exc_type)):
            raise translated_exc
