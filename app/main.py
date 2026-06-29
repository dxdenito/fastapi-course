from fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    stock: int
    description: str | None = None
    active: bool = True

app = FastAPI(
    title="FastAPI Course",
    description="Learning FastAPI via claude course"
)

@app.get("/")
def read_root():
    return {"message":"Welcome to Fastapi course"}


@app.get("/info")
def get_info():
    info = {
        "framework": "FastAPI",
        "python_version": "3.14.6",
        "developer": "Denis Kibathi Karanja"
    }

    return info


@app.get("/health")
async def health_check():
    health = {
        "status": "ok"
    }
    return health


@app.get("/products/{product_id}")
def get_product(product_id: int, ):
    product = {
        "id": product_id,
        "name": "Sample Product",
    }
    return product


@app.get("/search")
def search(query: str, limit: int = 5, active: bool | None = None):
    result = {
        "query": query,
        "limit": limit,
        "active": active
    }
    return result


@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, status: str | None = None, page: int = 1):
    orders = {
        "user_id": user_id,
        "status": status,
        "page": page
    }
    return orders

@app.post("/products")
def create_product(product: Product):
    res = {
        "product": product,
        "message": "Product created successfully"
    }
    return res


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, notify: bool = False):
    res = {
        "product_id": product_id,
        "product": product,
        "notify": notify
    }
    return res


@app.delete("/products/{product_id}")
def delete_product(product_id:int):
    res = {
        "message": f"Product {product_id} deleted",
        "success": True
    }
    return res