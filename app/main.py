from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from router.auth_router import auth_router
from router.product_router import product_router


app = FastAPI(debug=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(product_router)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
    # db_manager = UserManager()
    # product_manager = Product()
    # db_manager._create_db()
    # product_manager._create_db()
    uvicorn.run('main:app', port=8000, reload=True)