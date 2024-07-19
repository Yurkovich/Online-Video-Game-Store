from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from schemas.product_schema import CreateProduct
from model.product import ProductModel
from database.product_table import Product
from generator.card_generator import generate_product_html


product_router = APIRouter(tags=["Products"])
templates = Jinja2Templates(directory="templates")
product = Product()

class CreateProduct(BaseModel):
    product_name: str
    image_url: str
    genre: str
    price: int
    discount: int
    quantity: int
    is_displayed: bool = True

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    image_url: Optional[str] = None
    genre: Optional[str] = None
    price: Optional[int] = None
    discount: Optional[int] = None
    quantity: Optional[int] = None
    is_displayed: Optional[bool] = None

db_path = r"C:\Course work\app\database.db"

@product_router.get("/", response_model=List[ProductModel])
def show_products(request: Request):
    products = product.fetch_all_products()
    
    product_html_list = []
    for product_entry in products:
        product_html = generate_product_html({
            'image_url': product_entry[2],
            'product_name': product_entry[1],
            'genre': product_entry[3],
            'price': product_entry[4],
            'discount': product_entry[5]
        })
        product_html_list.append(product_html)

    return templates.TemplateResponse("index.html", {"request": request, "product_html_list": product_html_list})


@product_router.get("/products/{product_id}", response_model=ProductModel, summary="Получить товар по ID")
def read_product(product_id: int):
    db_path = r"C:\Course work\app\database.db"
    product_entry = Product.get_product_by_id(product_id, db_path)
    if product_entry is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product_entry

@product_router.post("/products/create/", response_model=CreateProduct, summary="Создать товар")
def create_product(product_data: CreateProduct, product_handler: Product = Depends()):
    try:
        product_handler.add_product(
        product_data.product_name,
        product_data.image_url,
        product_data.genre,
        product_data.price,
        product_data.discount,
        product_data.quantity,
        product_data.is_displayed
        )
        return product_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@product_router.put("/products/{product_id}/update/", summary="Обновить информацию о продукте")
def update_product(product_id: int, product_data: ProductUpdate, db_path: str = 'C:\\Course work\\app\\database.db'):
    try:
        Product.update_product(
            product_id,
            product_data.product_name,
            product_data.image_url,
            product_data.genre,
            product_data.price,
            product_data.discount,
            product_data.quantity,
            product_data.is_displayed,
            db_path
        )
        return {"message": f"Product with ID {product_id} has been updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@product_router.delete("/products/delete/{product_id}", summary="Удалить товар по ID")
def delete_product(product_id: int, product_handler: Product = Depends()):
    try:
        product_handler.delete_product(product_id)
        return {"message": f"Товар с ID '{product_id}' был удален"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
