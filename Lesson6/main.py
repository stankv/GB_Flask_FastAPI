from fastapi import FastAPI
import uvicorn
from app6 import app6

app = FastAPI()
app.mount("/Lesson6/", app6)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=False)
