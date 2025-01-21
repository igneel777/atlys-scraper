from typing import Generic

from _io import TextIOWrapper

from app.core.models.product import ProductInDB
from app.core.services.base import BaseService


class ProductService(BaseService[ProductInDB]):
    pass
