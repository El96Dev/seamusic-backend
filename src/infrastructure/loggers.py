from datetime import datetime
from enum import Enum
from logging import Logger as _Logger


class LogLevel(int, Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Logger(_Logger):
    def log(self, msg: str, level: LogLevel, *args, **kwargs) -> None:  # type: ignore[override, no-untyped-def]
        dt = datetime.now()
        text = f'[{dt.year}-{dt.month}-{dt.day} {dt.hour}:{dt.minute}:{dt.second}] #{level.name}    {__name__}: {self.name} - {msg}'
        super(Logger, self).log(level.value, text, *args, **kwargs)


app = Logger('app')
domain = Logger('domain')
infrastructure = Logger('infrastructure')
presentation = Logger('presentation')
