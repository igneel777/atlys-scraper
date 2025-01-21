from typing_extensions import Any
from pydantic import AnyHttpUrl
from abc import ABC, abstractmethod


class BaseFilestore(ABC):
    @abstractmethod
    def __init__(self, image_bucket_name:str):
        pass

    @abstractmethod
    def save_file_from_url(self, source_url:str, file_key:str):
        pass