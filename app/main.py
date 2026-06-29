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
        "framework": "fastapi",
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