from typing import List

import uvicorn
from fastapi import APIRouter, Body, FastAPI, Form

from experiments.form_json_body import FormToJSONRoute

router = APIRouter()
router.route_class = FormToJSONRoute


@router.get("/hello")
async def hello(params: List = Form([])):
    if params:
        return params

    return "hello"


@router.post("/hello")
async def hello_post_form(params: List = Form([])):
    if params:
        return params

    return "hello"


@router.post("/hello_body")
async def hello_post_body(params: List = Body([])):
    if params:
        return params

    return "hello"


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
