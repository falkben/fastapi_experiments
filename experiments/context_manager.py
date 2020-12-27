import time
from contextlib import contextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()


@contextmanager
def simple_context_manager(iterations=1000):
    """ this could be a wrapper around a database """

    def _gen():
        for i in range(iterations):
            yield str(i) + "\n"
            time.sleep(0.001)
            if i == iterations - 1:
                print("reached the end")

    try:
        yield _gen
    finally:
        # we could be closing the database conn here
        print("we are cleaning up")


def mock_db_query(iterations: int = 1000):
    """ Dependency wrapping a context manager """
    with simple_context_manager(iterations) as db:
        yield db


@app.get("/stream_context_mngr")
async def stream_context_mngr(iterations: int = 1000):
    with simple_context_manager(iterations) as gen:
        # ! this causes the finally block in the context manager to occur immediately *before* streaming the response
        # returning StreamingResponse causes the context man`ager to close for some reason
        return StreamingResponse(gen())


@app.get("/stream_dep")
async def stream_dep(db=Depends(mock_db_query)):
    """ could be sync or async path operator here
    This works as expected.  Finally block in the "wrapped" context manager occurs after the response is finished """
    return StreamingResponse(db())


@app.get("/direct_context_mngr")
async def direct_context_mngr(iterations: int = 1000):
    """ No StreamingResponse -- this works (finally block executed last) """
    with simple_context_manager(iterations) as gen:
        return HTMLResponse("".join(gen()))


@app.get("/file_context_mngr_stream")
async def file_context_mngr_stream():
    """ This fails because file is closed when it goes to stream """
    with open(f"{__file__}") as f:
        return StreamingResponse(f)


@app.get("/file_context_mngr_direct")
async def file_context_mngr_direct():
    """ this works because no streamingresponse """
    with open(f"{__file__}") as f:
        return HTMLResponse(f.read())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
