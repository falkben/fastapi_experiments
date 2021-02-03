import asyncio

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    age: int


@app.post("/hello")
def hello(user: User):
    return f"hello {user.name}, you are {user.age} years old"


async def get_form(request: Request):
    # not used, but how to return form data
    return await request.form()


async def get_json(request: Request):
    return await request.json()


@app.post("/goodbye")
def goodbye(body=Depends(get_json)):
    user = User(**body)
    return f"bye {user.name}, you are {user.age} years old"


@app.post("/lunchtime")
def lunchtime(request: Request):
    body = asyncio.run(request.json())
    # equivalent to in this case:
    # loop = asyncio.new_event_loop()
    # body = loop.run_until_complete(request.json())
    user = User(**body)
    return f"it's lunchtime!!! {user.name}, you are {user.age} years old"


client = TestClient(app)


def test_hello():
    resp = client.post("/hello", json={"name": "bob", "age": 300})
    assert resp.status_code == 200
    assert resp.json() == "hello bob, you are 300 years old"


def test_goodbye():
    resp = client.post("/goodbye", json={"name": "bob", "age": 300})
    assert resp.status_code == 200
    assert resp.json() == "bye bob, you are 300 years old"


def test_lunchtime():
    resp = client.post("/lunchtime", json={"name": "bob", "age": 300})
    assert resp.status_code == 200
    assert resp.json() == "it's lunchtime!!! bob, you are 300 years old"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
