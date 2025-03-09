from abc import ABC


class BaseInterface(ABC):
    def __init__(self) -> None:
        raise TypeError("TypeError: Can't instantiate abstract class BaseInterface")
