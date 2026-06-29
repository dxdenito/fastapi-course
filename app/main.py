from fastapi import FastAPI

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