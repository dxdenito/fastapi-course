from fastapi import FastAPI

from app.routers import positions, products, trades, backtest

app = FastAPI(title="FastAPI Course", description="Learning FastAPI via Claude Course")


app.include_router(trades.router)
app.include_router(positions.router)
app.include_router(products.router)
app.include_router(backtest.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Course"}


@app.get("/info")
def get_info():
    return {
        "framework": "FastAPI",
        "python_version": "3.14.6",
        "developer": "Denis Kibathi Karanja",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}
