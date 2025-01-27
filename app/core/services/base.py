import json
from typing import Generic, Type, TypeVar

from _io import TextIOWrapper
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseService(Generic[ModelType]):
    """Base Service to inherit from"""

    def __init__(self, db_connection: TextIOWrapper, model: Type[ModelType]):
        self.db_connection = db_connection
        self.model_class: Type[ModelType] = model

    def insert_in_db(self, obj: ModelType):
        self.db_connection.seek(0)
        model_name = self.model_class.__name__
        if not isinstance(obj, self.model_class):
            raise RuntimeError(f"Object is not of type {model_name}")

        data_in_file: dict = json.load(self.db_connection)
        data_in_file.setdefault(model_name, []).append(obj.model_dump(mode="json"))
        self.db_connection.seek(0)
        json.dump(data_in_file, self.db_connection, ensure_ascii=False, indent=4)
        self.db_connection.flush()

    def insert_in_db_bulk(self, obj_list: list[ModelType]):
        self.db_connection.seek(0)
        model_name = self.model_class.__name__
        insert_list = []
        for obj in obj_list:
            if not isinstance(obj, self.model_class):
                raise RuntimeError(f"Object is not of type {model_name}")
            insert_list.append(obj.model_dump(mode="json"))

        data_in_file: dict = json.load(self.db_connection)
        data_in_file.setdefault(model_name, []).extend(insert_list)
        self.db_connection.seek(0)
        json.dump(data_in_file, self.db_connection, ensure_ascii=False, indent=4)
        self.db_connection.flush()
