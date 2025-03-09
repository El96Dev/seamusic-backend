from dataclasses import dataclass
from types import TracebackType

from fastapi import HTTPException

from src.infrastructure.exceptions import Exc


@dataclass
class ExceptionHandler:
    """
    Class for handling exceptions on API level. Usually, the exceptions
    are raised on lower layers, so API-layer has to convert them into
    client-friendly ones. Can only be used via an asynchronous context
    manager

    :param exceptions: dictionary mapping low-level exception types to
      client-friendly ones
    """

    exceptions: dict[type[Exc], HTTPException]

    async def __aenter__(self) -> "ExceptionHandler":
        """
        :return Self: instance returns itself when entering an
          asynchronous context manager
        """

        return self

    async def __aexit__(
        self,
        exc_type: type[Exc] | None,
        exc_val: Exc | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Method to handle low-level exceptions and raise client-friendly
        ones

        :param exc_type: exception type
        :param exc_val: exception instance
        :param exc_tb: full traceback
        :raise HTTPException: when low-level exception was handled
        """

        if exc_type and exc_val and (translated_exc := self.exceptions.get(exc_type)):
            raise translated_exc
