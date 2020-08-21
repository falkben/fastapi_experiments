from typing import Optional
import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    p_int: Optional[int] = None
    p_float: Optional[float] = None
    p_str: Optional[str] = None


class BodyOrQuery:
    def __init__(self, item: Item = None, query: Item = Depends()):
        # merging here

        item_dict = {}
        if item is not None:
            item_dict = item.dict()

        self.items = {
            **{k: v for k, v in item_dict.items() if v is not None},
            **{k: v for k, v in query.dict().items() if v is not None},
        }


@app.post("/")
def body_or_query_using_depends(body_or_query: BodyOrQuery = Depends()):
    return body_or_query.items


@app.post("/body_or_query")
def body_or_query(
    item: Optional[Item] = None,
    p_int: Optional[int] = None,
    p_float: Optional[float] = None,
    p_str: Optional[str] = None,
):
    """ Can take query params or json data with the same name.
    Probably cleaner to use the other approach with the Depends """
    query_data = {"p_int": p_int, "p_float": p_float, "p_str": p_str}

    item_dict = {}
    if item is not None:
        item_dict = item.dict()

    merge_data = {
        **{k: v for k, v in query_data.items() if v is not None},
        **{k: v for k, v in item_dict.items() if v is not None},
    }

    return merge_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
