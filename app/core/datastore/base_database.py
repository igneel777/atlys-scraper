from abc import ABC, abstractmethod

from typing_extensions import Any


class BaseDatabase(ABC):
    connection: Any = None

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass
