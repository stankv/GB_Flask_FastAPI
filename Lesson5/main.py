from fastapi import FastAPI
from uvicorn import run
from Lesson5.task_1.app1 import app1
from Lesson5.task_2.app2 import app2
from Lesson5.task_3_4_5.app3 import app3
from Lesson5.task_6.app6 import app6
from Lesson5.task_7.app7 import app7
from Lesson5.task_8.app8 import app8

app = FastAPI()
app.mount('/task_1/', app1)
app.mount('/task_2/', app2)
app.mount('/task_3_4_5/', app3)
app.mount('/task_6/', app6)
app.mount('/task_7/', app7)
app.mount('/task_8/', app8)


@app.get('/')
async def root():
    return {"message": "Hello world!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    run("main:app", host='127.0.0.1', port=8000, reload=True)
