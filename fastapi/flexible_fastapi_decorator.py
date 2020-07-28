""" flexible decorator around fastapi routes
call with: `uvicorn flexible_fastapi_decorator:app --reload` or `python flexible_fastapi_decorator.py` """

import uvicorn
from fastapi import FastAPI
import asyncio
import functools
import time
from contextlib import contextmanager

"""
from stackoverflow: https://stackoverflow.com/q/44169998/532963
"""


def duration(func):
    """ decorator that can take either coroutine or normal function """
    @contextmanager
    def wrapping_logic():
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return (await func(*args, **kwargs))
            return tmp()
    return wrapper


app = FastAPI()


@app.get("/hello")
@duration
def slow_hello(sleep_time=.5):
    """ route that uses a flexible decorator """

    print("normal function sleeps for:", sleep_time)
    time.sleep(sleep_time)
    print("normal waited")
    return {"message": "slow hello"}


@app.get("/async_hello")
@duration
async def slow_async_hello(sleep_time=.75):
    print("coroutine sleeps for:", sleep_time)
    await asyncio.sleep(sleep_time)
    print('coroutine waited')
    return {"message": "slow async hello"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
