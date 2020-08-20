import time
from contextlib import contextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import StreamingResponse

app = FastAPI()


@contextmanager
def simple_context_manager():
    """ this could be a wrapper around a database """

    def _gen():
        iterations = 1000
        for i in range(iterations):
            yield str(i)
            time.sleep(0.001)
            if i == iterations - 1:
                print("reached the end")

    try:
        yield _gen
    finally:
        # we could be closing the database conn here
        print("we are cleaning up")


def mock_db_query():
    """ Dependency wrapping a context manager """
    with simple_context_manager() as db:
        yield db


@app.get("/stream_context_mngr")
async def stream_context_mngr():
    with simple_context_manager() as gen:
        # ! this causes the finally block in the context manager to occur immediately *before* streaming the response
        # returning StreamingResponse causes the context manager to close for some reason
        return StreamingResponse(gen())


@app.get("/stream_dep")
async def stream_dep(db=Depends(mock_db_query)):
    """ could be sync or async path operator here 
    This works as expected.  Finally block in the "wrapped" context manager occurs after the response is finished """
    return StreamingResponse(db())


@app.get("/direct_context_mngr")
async def direct_context_mngr():
    with simple_context_manager() as gen:
        # ! This also seems to result in the finally block executing before the response is returned or the generator is consumed
        return gen()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
