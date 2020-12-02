import uvicorn
from fastapi import FastAPI, Form, Depends, Header, Request, Response
from fastapi.responses import RedirectResponse
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


async def redirect_to_json(content_type: str = Header(None)):
    if content_type == "application/json":
        raise RedirectJSONException


@app.post("/form", dependencies=[Depends(redirect_to_json)])
def form_endpoint(
    user: UserFormData = Depends(UserFormData),
):
    return user


@app.post("/json")
def json_endpoint(user: UserData):
    return user


class RedirectJSONException(Exception):
    pass


@app.exception_handler(RedirectJSONException)
async def exception_handler(request: Request, exc: RedirectJSONException) -> Response:
    return RedirectResponse(url="/json")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
