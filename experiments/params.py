from typing import Optional
import uvicorn
from fastapi import FastAPI, Query, Request, Depends
from pydantic import BaseModel

app = FastAPI()


@app.get("/hello")
def hello(request: Request, sleep_time: int = Query(None)):
    query_params = request.query_params.items()
    return query_params


class Item(BaseModel):
    p_int: Optional[int] = None
    p_float: Optional[float] = None
    p_str: Optional[str] = None


@app.get("/conv")
@app.post("/conv")
def conversions(
    item: Optional[Item] = None,
    p_int: Optional[int] = None,
    p_float: Optional[float] = None,
    p_str: Optional[str] = None,
):
    """ Can take query params or json data with the same name """
    query_data = {"p_int": p_int, "p_float": p_float, "p_str": p_str}

    item_dict = {}
    if item is not None:
        item_dict = item.dict()

    merge_data = {
        **{k: v for k, v in query_data.items() if v is not None},
        **{k: v for k, v in item_dict.items() if v is not None},
    }

    return merge_data


class BodyOrQuery:
    def __init__(self, item: Item = None, query: Item = Depends()):
        self.items = {"item": item, "query": query}  # merge everything here


# WIP re: body/query combination
# this shows request Body in swagger for GET which is not ideal
# still requires a manual merge of the data
@app.post("/")
@app.get("/")
def home(body_or_query: BodyOrQuery = Depends()):
    return body_or_query


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
