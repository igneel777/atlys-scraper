from datetime import datetime, timezone
from pydantic import BaseModel, AnyHttpUrl, field_validator
import re

class ProductInDB(BaseModel):
    price: float
    product_name: str
    image_url: AnyHttpUrl
    image_key: str
    scraped_at: datetime = datetime.now(timezone.utc)

    @field_validator('price', mode='before')
    @classmethod
    def extract_float(cls, price: str):
        match = re.match(r'₹([\d.]+)', price)
        if match:
            amount = float(match.group(1))
        else:
            amount = 0.0
        return amount
