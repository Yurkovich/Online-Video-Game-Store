from fastapi import APIRouter, Request
from typing import List
from fastapi.templating import Jinja2Templates

from model.product import ProductModel
from database.product_table import Product
from generator.card_generator import generate_product_html

product_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@product_router.get("/products/", response_model=List[ProductModel])
async def show_products(request: Request):
    product_manager = Product()
    products = product_manager.fetch_all_products()
    
    product_html_list = []
    for product in products:
        product_html = generate_product_html({
            'image_url': product[2],
            'product_name': product[1],
            'genre': product[3],
            'price': product[4],
            'discount': product[5]
        })
        product_html_list.append(product_html)

    return templates.TemplateResponse("index.html", {"request": request, "product_html_list": product_html_list})