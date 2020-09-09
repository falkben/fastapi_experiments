import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def get():
    return "hello"


@app.post("/hello")
async def post():
    return "hello"


@app.get("/")
async def get_bare():
    return "hello"


@app.post("/")
async def post_bare():
    return "hello"


@app.post("/hello_hello")
@app.post("/hello_hello/")
async def double_post():
    return "hello"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
