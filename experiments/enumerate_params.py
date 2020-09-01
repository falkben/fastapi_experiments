from enum import Enum

import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()


class NameEnum(str, Enum):
    empty = ""
    bob = "bob"
    doug = "doug"


@app.get("/hello")
async def hello(name: NameEnum = Query(NameEnum.empty, alias="first_name")):
    return "hello " + name.value


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
