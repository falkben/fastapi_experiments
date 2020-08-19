from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, Header, Query, Request

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


def common_db_args(
    request: Request,
    flatten_response: bool = True,
    accept: str = Header(None),
    param_format: str = Query("", alias="format"),
    delimiter: Optional[str] = None,
    raw: bool = False,
    include_info: bool = True,
):
    """ Dependency for common db arguments

    Note: most of these are for `stream_data` and could be moved into their own dependency if desired

    To use in code:

    @app.get("/")
    def get(commons: dict = Depends(service.common_db_args)):
        ...
    """

    path_format = request.url.path

    if delimiter is not None:
        delimiter = delimiter.lower()
    if accept is not None:
        accept = accept.lower()

    return {
        "flatten_response": flatten_response,
        "accept": accept.lower(),
        "param_format": param_format.lower(),
        "format_delimiter": delimiter,
        "raw": raw,
        "include_info": include_info,
        "path_format": path_format.lower(),
    }


def common_paginate_args(
    page: int = 1, pagesize: int = 50000, commons: dict = Depends(common_db_args)
):
    """
    Dependency for paginated db args. Includes common_db_args as well

    To use in code:

    @app.get("/")
    def get(commons_paginate: dict = Depends(service.common_paginate_args)):
        ...
    """
    return {"page": page, "pagesize": pagesize, **commons}


@app.get("/common_db_args")
def common_db_args(commons: dict = Depends(common_db_args)):
    return commons


@app.get("/common_db_paginate_args")
def common_db_paginate_args(commons: dict = Depends(common_paginate_args)):
    return commons


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
