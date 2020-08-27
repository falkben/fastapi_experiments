""" example taking list with square brackets like tornado lets you do """

from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, Query
from pydantic import Json
from starlette.responses import StreamingResponse

app = FastAPI()


@app.get("/hello")
def hello(names: List[str] = Query(None)):
    """ list param method """

    if names is not None:
        return StreamingResponse((f"Hello {name}" for name in names))
    else:
        return {"message": "no names"}


def parse_list(
    names: List[str] = Query(None, description="List of names to greet")
) -> Optional[List]:
    """
    accepts strings formatted as lists with square brackets
    names can be in the format
    "[bob,jeff,greg]" or '["bob","jeff","greg"]'
    """

    def remove_prefix(text: str, prefix: str):
        return text[text.startswith(prefix) and len(prefix) :]

    def remove_postfix(text: str, postfix: str):
        if text.endswith(postfix):
            text = text[: -len(postfix)]
        return text

    if names is None:
        return

    # we already have a list, we can return
    if len(names) > 1:
        return names

    # if we don't start with a "[" and end with "]" it's just a normal entry
    flat_names = names[0]
    if not flat_names.startswith("[") and not flat_names.endswith("]"):
        return names

    flat_names = remove_prefix(flat_names, "[")
    flat_names = remove_postfix(flat_names, "]")

    names_list = flat_names.split(",")
    names_list = [remove_prefix(n.strip(), '"') for n in names_list]
    names_list = [remove_postfix(n.strip(), '"') for n in names_list]

    return names_list


@app.get("/hello_list")
def hello_list(names: List[str] = Depends(parse_list)):
    """ list param method """

    if names is not None:
        return StreamingResponse((f"Hello {name}" for name in names))
    else:
        return {"message": "no names"}


@app.get("/json_list/")
def json_list(names: Json = Query([])):
    """ Use pydantic type parse the query string as JSON

    names=["Bob", "Jeff"] is parsed into a Python list because the JSON parser can read that

    However, it fails if the user supplies a string that isn't valid JSON

    names='"Bob", "Jeff"' raises a validation error, though

    Possibly with some regex we could enforce passing a list this way

    """
    if names is not None:
        return StreamingResponse((f"Hello {name}" for name in names))
    else:
        return {"message": "no names"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
