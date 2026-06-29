from fastapi import FastAPI

app = FastAPI(
    title="FastAPI course",
    description="Learning FastAPI via claude course"
)

@app.get("/")
def read_root():
    return {"message":"Welcome to Fastapi course"}