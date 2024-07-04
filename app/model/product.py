from pydantic import BaseModel

class ProductModel(BaseModel):
    id: int
    product_name: str
    image_url: str
    genre: str
    price: int
    discount: int
    quantity: int
    is_displayed: bool