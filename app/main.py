from fastapi import FastAPI
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    stock: int
    description: str | None = None
    active: bool = True

class Trade(BaseModel):
    pair: str
    direction: str
    entry_price: float
    stop_loss: float
    take_profit: float
    lot_size: float = 0.01
    notes: str | None = None


app = FastAPI(
    title="FastAPI Course",
    description="Learning FastAPI via Claude Course"
)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Course"}


@app.get("/info")
def get_info():
    return {
        "framework": "FastAPI",
        "python_version": "3.14.6",
        "developer": "Denis Kibathi Karanja"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "id": product_id,
        "name": "Sample Product"
    }


@app.get("/search")
def search(query: str, limit: int = 5, active: bool | None = None):
    return {
        "query": query,
        "limit": limit,
        "active": active
    }


@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, status: str | None = None, page: int = 1):
    return {
        "user_id": user_id,
        "status": status,
        "page": page
    }


@app.post("/products")
def create_product(product: Product):
    return {
        "product": product,
        "message": "Product created successfully"
    }


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, notify: bool = False):
    return {
        "product_id": product_id,
        "product": product,
        "notify": notify
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {
        "message": f"Product {product_id} deleted",
        "success": True
    }


#MODULE 1 FINAL TEST ENDPOINTS


@app.get("/trades")
def get_trades():
    return [
        {
            "pair": "EURUSD",
            "direction": "buy",
            "entry_price": 1.1056,
            "stop_loss": 1.1046,
            "take_profit": 1.2546,
            "lot_size": 2,
            "notes": "I am feeling positive and I followed my rules"
        },
        {
            "pair": "EURJPY",
            "direction": "sell",
            "entry_price": 156.105,
            "stop_loss": 156.200,
            "take_profit": 145.254,
            "lot_size": 2,
            "notes": "I am not feeling confident but I followed my rules"
        }
    ]


@app.get("/trades/summary")
def get_summary(pair: str | None = None, direction: str | None = None):
    return {
        "pair": pair,
        "direction": direction,
        "total_trades": 0
    }


@app.get("/trades/{trade_id}")
def get_trade(trade_id: int):
    return {
        "trade_id": trade_id,
        "pair": "EURUSD"
    }


@app.post("/trades")
def log_trade(trade: Trade):
    return {
        "trade": trade,
        "message": "Trade logged"
    }


@app.delete("/trades/{trade_id}")
def delete_trade(trade_id: int):
    return {
        "message": f"Trade {trade_id} removed",
        "success": True
    }
