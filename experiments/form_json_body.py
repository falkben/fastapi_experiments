import uvicorn
from fastapi import FastAPI, Form, Depends
from pydantic import BaseModel

app = FastAPI()


def form_body(cls):
    # from https://github.com/tiangolo/fastapi/issues/1989#issuecomment-684799715
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


class UserData(BaseModel):
    name: str
    greeting: str


@form_body
class UserFormData(UserData):
    ...


@app.post("/form")
def form_endpoint(user: UserFormData = Depends(UserFormData)):
    return user


@app.post("/json")
def json_endpoint(user: UserData):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
