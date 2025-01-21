from _io import TextIOWrapper

from app.core.models import ProductInDB
from app.core.services import ProductService


def get_product_service(db: TextIOWrapper) -> ProductService:
    return ProductService(db, ProductInDB)
