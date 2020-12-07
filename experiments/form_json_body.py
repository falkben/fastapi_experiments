import json
from typing import Callable

import fastapi.params
import uvicorn
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    Form,
    Header,
    Query,
    Request,
    Response,
    params,
)
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel
from starlette.routing import Match


class FormToJSONRequest(Request):
    """Custom request which converts form input to JSON for JSON post endpoints
    It reads content-type header of request to see if it's form data
    If it's a form request it checks the matched route and converts the form data
    to JSON"""

    async def body(self) -> bytes:
        """ Overwrite body method """
        if not hasattr(self, "_body"):

            # only if request content-type is form
            if self.headers.get("content-type", None) in [
                "multipart/form-data",
                "application/x-www-form-urlencoded",
            ]:

                # find matching route and body_field
                body_field = None
                for route in self.app.routes:
                    match, _ = route.matches(self.scope)
                    if match == Match.FULL:
                        body_field = route.body_field
                        break

                # if matching route has body field & is not form
                if body_field and not isinstance(
                    body_field.field_info, fastapi.params.Form
                ):
                    form = await self.form()
                    del self._form
                    form_dict = dict(form)
                    body = json.dumps(form_dict).encode("utf-8")
                    self._body = body
                    # we might as well store it now while it's a dict
                    self._json = form_dict
                    return self._body

            body = await super().body()
            self._body = body

        return self._body


class FormToJSONRoute(APIRoute):
    """Custom Route Class for converting Form data to JSON

    Example:

    ```python
    router = APIRouter()
    router.route_class = util.FormToJSONRoute
    ```

    Any @router.post path operators that take JSON data will have form input
    automatically converted to JSON

    See
    https://fastapi.tiangolo.com/advanced/custom-request-and-route/#handling-custom-request-body-encodings
    """

    def get_route_handler(self) -> Callable:
        """ overwrite get_route_handler with FormToJSONRequest """
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = FormToJSONRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()

# isolating the redirect exception handling from form parsing
router = APIRouter()


def modify_field_signature(cls, field_type):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(
                default=field_type(...)
                if arg.default is arg.empty
                else field_type(arg.default)
            )
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


def form_body(cls):
    # from https://github.com/tiangolo/fastapi/issues/1989#issuecomment-684799715
    return modify_field_signature(cls, Form)


def query_param(cls):
    # from https://github.com/tiangolo/fastapi/issues/1989#issuecomment-684799715
    return modify_field_signature(cls, Query)


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


@router.post("/form", dependencies=[Depends(redirect_to_json)])
def form_endpoint(
    user: UserData = Depends(UserFormData),
):
    return user


@router.post("/json")
def json_endpoint(user: UserData):
    return user


@router.get("/query")
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


# isolating on a separater router to make testing a little more obvious
form_to_json_router = APIRouter(prefix="/form_to_json")
form_to_json_router.route_class = FormToJSONRoute


@form_to_json_router.post("/form")
def form_to_json_form_endpoint(user: UserData = Depends(UserFormData)):
    return user


@form_to_json_router.post("/json")
def form_to_json_json_endpoint(user: UserData):
    return user


@form_to_json_router.get("/query")
def form_to_json_query_endpoint(user: UserData = Depends(UserQueryData)):
    return user


app.include_router(router)
app.include_router(form_to_json_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
