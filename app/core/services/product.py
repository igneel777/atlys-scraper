from typing import Generic
from _io import TextIOWrapper

from app.core.services.base import BaseService
from app.core.models.product import ProductInDB

class ProductService(BaseService[ProductInDB]):
    pass