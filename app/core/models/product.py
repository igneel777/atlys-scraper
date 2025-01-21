from datetime import datetime, timezone

from pydantic import AnyHttpUrl, BaseModel


class ProductInDB(BaseModel):
    price: float
    product_name: str
    image_url: AnyHttpUrl
    image_key: str
    scraped_at: datetime = datetime.now(timezone.utc)
