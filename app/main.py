from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from database.user_table import UserManager
from database.product_table import Product

from router.auth_router import router
from router.product_router import product_router


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
app.include_router(product_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
    db_manager = UserManager()
    product_manager = Product()
    db_manager._create_db()
    product_manager._create_db()
    product_manager.add_product('For Honor', 'app\static\images\gta5-card.jpg', 'Action', 2499, 20, 100, 1)
    uvicorn.run('main:app', port=8000, reload=True)

# product_name, image_url, genre, price, discount, quantity, is_displayed
# 'For Honor', 'app\static\images\gta5-card.jpg', 'Action', 2499, 20, 100, 1