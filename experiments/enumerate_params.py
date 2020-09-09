from enum import Enum
from typing import Optional

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


animals_dict = {"ANT": "walk", "BEE": "flies", "CAT": "meows", "DOG": "barks"}
Animal = Enum("Animal", {k: k for k in animals_dict})


@app.get("/animal")
async def animal(anim: Optional[Animal] = Query(None)):
    if anim is not None:
        return anim.name
    else:
        return "not found"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
