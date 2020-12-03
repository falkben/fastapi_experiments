import uvicorn
from fastapi import Depends, FastAPI, Form, Header, Query, Request, Response, params
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
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


def query_param(cls):
    # from https://github.com/tiangolo/fastapi/issues/1989#issuecomment-684799715
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Query(...))
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


@query_param
class UserQueryData(UserData):
    ...


async def redirect_to_json(content_type: str = Header(None)):
    if content_type == "application/json":
        raise RedirectException("/json")


async def redirect_to_form(content_type: str = Header(None)):
    if content_type != "application/json":
        raise RedirectException("/form")


@app.post("/form", dependencies=[Depends(redirect_to_json)])
def form_endpoint(
    user: UserData = Depends(UserFormData),
):
    return user


@app.post("/json", dependencies=[Depends(redirect_to_form)])
def json_endpoint(user: UserData):
    return user


@app.get("/query")
def query_endpoint(user: UserData = Depends(UserQueryData)):
    return user


class RedirectException(Exception):
    def __init__(self, url: str) -> None:
        self.url = url


@app.exception_handler(RedirectException)
async def exception_handler(request: Request, exc: RedirectException) -> Response:
    return RedirectResponse(url=exc.url)


@app.exception_handler(RequestValidationError)
async def json_request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> Response:

    # get the current route of the request
    # then check the body_field of the route (as in fastapi.routing):
    # `body_field and isinstance(body_field.field_info, params.Form)`
    routes = [r.path for r in request.app.routes]
    body_field = None
    if request.url.path in routes:
        route_index = routes.index(request.url.path)
        # body_field is None for get requests
        body_field = request.app.routes[route_index].body_field

    if (
        body_field
        and not isinstance(body_field.field_info, params.Form)
        and request.headers.get("content-type") != "application/json"
        # we could check for a specific endpoint:
        # request.url.path == "/json"
        # could also check for the type of error:
        # exc.errors()[0]["type"] == "value_error.jsondecode"
    ):
        # we should redirect to the form endpoint
        return RedirectResponse(url="/form")
    else:
        # otherwise we just have a bad request and we do the normal thing
        return await request_validation_exception_handler(request, exc)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
