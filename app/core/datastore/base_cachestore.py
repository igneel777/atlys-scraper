from abc import ABC, abstractmethod
from typing import Any


class BaseCacheStore(ABC):
    store: Any

    @abstractmethod
    def set_values(self, key: str, value, expiry: dict[str, Any]) -> dict[str, Any]:
        """Save recent values to cache"""

    @abstractmethod
    def get_values(self, key: str) -> dict[str, Any] | list[Any] | None:
        """Get values from cache"""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove the specified key from cache"""
