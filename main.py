from fastapi import FastAPI
import uvicorn

from fastapi.staticfiles import StaticFiles

from api.Routes.productsRoute import productRoutes
from api.Routes.defaultRoute import defaultRoute

app = FastAPI(title="FastAPI-Products-Backend", description="CRUD API")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(productRoutes, tags=["Porducts"], prefix="/api/products")
app.include_router(defaultRoute)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
