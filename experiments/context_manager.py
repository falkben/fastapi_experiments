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


def db_query():
    """ Dependency wrapping a context manager """
    with hello_context_manager() as db:
        yield db


@app.get("/hello")
async def hello():
    with hello_context_manager() as gen:
        # ! DO NOT USE THIS, USE DEPENDENCY INSTEAD
        # ! this causes the finally block to occur immediately
        # returning StreamingResponse causes the context manager to close for some reason
        return StreamingResponse(gen())


@app.get("/hello_dep")
async def hello_dep(db=Depends(db_query)):
    """ could be sync or async path operator here """
    return StreamingResponse(db())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
