from typing import List

import uvicorn
from fastapi import FastAPI, Form

app = FastAPI()


@app.get("/hello")
async def hello(params: List = Form([])):
    if params:
        return params

    return "hello"


@app.post("/hello")
async def hello_post(params: List = Form([])):
    if params:
        return params

    return "hello"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
