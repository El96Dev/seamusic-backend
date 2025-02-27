from fastapi import HTTPException

from src.infrastructure.exceptions import Exc


class ExceptionHandler:
    """
    Class for handling exceptions in API level.
    Usually, exceptions are raised on lower layers,
    so API-layer has to convert them into
    client-friendly ones
    """

    def __init__(self, exceptions: dict[type[Exc], HTTPException]):
        """
        :param exceptions: dictionary with low-level exceptions
          specified as keys and client-friendly exceptions
          specified as values
        """
        self.exceptions = exceptions

    async def __aenter__(self):
        try:
            yield self
        except Exc as e:
            exc: HTTPException | None = self.exceptions.get(type(e))
            if exc:
                raise exc
