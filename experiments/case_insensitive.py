import uvicorn
from fastapi import FastAPI, Query, Request
from fastapi.testclient import TestClient
from starlette.datastructures import QueryParams

app = FastAPI()


@app.get("/hello")
async def hello(
    ra: float = Query(..., alias="RA"),
    dec: float = Query(..., alias="DEC"),
):
    return {"ra": ra, "dec": dec}


@app.middleware("http")
async def uppercase_params(request: Request, call_next):

    query_params = request.query_params
    query_params_upper = QueryParams({k.upper(): v for k, v in query_params.items()})

    # only scope/state are carried through
    request.scope["query_string"] = bytes(str(query_params_upper), "ascii")

    return await call_next(request)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


client = TestClient(app)


def test_hello():
    resp = client.get("/hello?rA=1&dec=1")
    assert resp.status_code == 200
    assert resp.json() == {"ra": 1, "dec": 1}
