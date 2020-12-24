import time
from itertools import chain

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


def check_one():
    # check 1
    time.sleep(1)
    yield "passed 1\n"


def check_two():
    # check 2
    time.sleep(1)
    yield "passed 2\n"


def check_three():
    # check 3
    time.sleep(1)
    yield "passed 3\n"


app = FastAPI()


@app.get("/status", response_model=str)
def status():
    gen1 = check_one()
    gen2 = check_two()
    gen3 = check_three()
    return StreamingResponse(chain(gen1, gen2, gen3, ["done"]))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
