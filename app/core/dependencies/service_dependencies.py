from _io import TextIOWrapper

from app.core.services import ProductService
from app.core.models import ProductInDB

def get_product_service(db:TextIOWrapper)->ProductService:
    return ProductService(db, ProductInDB)
