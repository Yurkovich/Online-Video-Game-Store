
from pydantic import BaseModel


class CreateProduct(BaseModel):
    product_name: str
    image_url: str
    genre: str
    price: int
    discount: int = 0
    quantity: int = 0
    is_displayed: bool = True