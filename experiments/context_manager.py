from contextlib import contextmanager
import time

from fastapi.params import Depends
from starlette.responses import StreamingResponse

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@contextmanager
def hello_context_manager():
    def _gen():
        for i in range(1000):
            yield str(i)
            time.sleep(0.001)

    try:
        yield _gen
    finally:
        print("we are cleaning up")
        del _gen  # trying to simulate a db close


def db_query():
    def _db():
        for i in range(1000):
            yield str(i)
            time.sleep(0.001)

    try:
        yield _db
    finally:
        print("we are cleaning up")
        del _db


@app.get("/hello")
def hello():
    with hello_context_manager() as gen:
        # ! this causes the finally block to occur immediately but somehow doesn't fail?
        return StreamingResponse(gen())


@app.get("/hello_dep")
def hello_dep(gen: db_query = Depends()):
    return StreamingResponse(gen())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
