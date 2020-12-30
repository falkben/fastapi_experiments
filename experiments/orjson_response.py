import inspect
from datetime import datetime
from functools import wraps
from typing import Any, List

import orjson
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, Response
from pydantic import BaseModel


def datetime_parser(obj):
    """ custom parser for orjson (usually named default) """
    if isinstance(obj, datetime):
        return str(obj)
    raise TypeError


class CustomORJSONResponse(ORJSONResponse):
    """ custom orjson response with a custom format for datetimes

    orjson defaults to outputing datetime objects in RFC 3339 format:
        `1970-01-01T00:00:00+00:00`

    with this, we simply output the string representation of the python datetime object
        `1970-01-01 00:00:00`

    see: https://github.com/ijl/orjson#opt_passthrough_datetime
    """

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(
            content, option=orjson.OPT_PASSTHROUGH_DATETIME, default=datetime_parser
        )


app = FastAPI()

# some "large" content to exercise the json parsing
CONTENT = {
    "results": {
        "dates": [datetime.now() for _ in range(10000)],
        "numbers": list(range(10000)),
    }
}


# pydantic response models, only used for overriding the json encoder
class ContentData(BaseModel):
    dates: List[datetime]
    numbers: List[float]


class ContentItem(BaseModel):
    results: ContentData

    class Config:
        json_encoders = {
            datetime: lambda v: str(v),
        }


def go_fast(f):
    """Skips FastAPI's slow `jsonable_encoder` and `serialize_response` and converts
    content not wrapped in a response into a ORJSONResponse w/ custom datetime
    serialization """

    @wraps(f)
    async def a_wrapped(*args, **kwargs):
        return CustomORJSONResponse(await f(*args, **kwargs))

    @wraps(f)
    def wrapped(*args, **kwargs):
        return CustomORJSONResponse(f(*args, **kwargs))

    if inspect.iscoroutinefunction(f):
        return a_wrapped
    else:
        return wrapped


@app.get("/a", response_class=CustomORJSONResponse, response_model=ContentItem)
async def orjson_response_class_with_response_model():
    """ By specifying a response model we can use custom serialization

    This is still lsow, since we still call `jsonable_encoder` & `serialize_response` 
    before converting to the ORJSONResponse class.

    By setting response_model, OpenAPI documentation shows more info, but it doesn't
    seem to use the custom json encoder we specified when displaying the example. This
    may be a limitation of the UI (SwaggerUI) as I don't actually see any example data
    in the schema itself.

    Unclear if setting response_class really has much of an effect since we serialize
    it ourselves anways
    """
    return CONTENT


@app.get("/f", response_class=CustomORJSONResponse, response_model=ContentItem)
async def orjson_response_class_with_response_model_return_response():
    """ Same as /a but wrapping the content around response object CustomORJSONResponse
    which allows it to return quickly (doesn't invoke `jsonable_encoder`)
    """
    return CustomORJSONResponse(CONTENT)


@app.get("/b")
async def direct_orjson_response():
    """ Directly returns the orjson response
    You don't need the response_class or response_model
    """
    return CustomORJSONResponse(CONTENT)


@app.get("/c")
@go_fast
async def fast_orjson_response():
    """ async endpoint that uses decorator to convert dictionary to Response type using
    ORJSONResponse """
    return CONTENT


@app.get("/d")
@go_fast
def sync_fast_orjson_response():
    """ normal (not async) endpoint that uses decorator to convert dictionary to
    Response type using ORJSONResponse """
    return CONTENT


@app.get("/e")
async def json_response():
    """ manually dumping orjson data and returning it w/ Response
    Since our app specified a default JSONResponse as response_class, it still says we
    return application/json in openapi spec. (this would go away if you set
    `response_class=Response` on the path operator decorator)
    """
    string_content = orjson.dumps(
        CONTENT, option=orjson.OPT_PASSTHROUGH_DATETIME, default=datetime_parser
    )
    return Response(string_content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
