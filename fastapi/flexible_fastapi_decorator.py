""" flexible decorator around fastapi routes
call with: `uvicorn flexible_fastapi_decorator:app --reload` or `python flexible_fastapi_decorator.py`
stackoverflow: https://stackoverflow.com/q/44169998/532963
"""

import asyncio
import functools
import time

import aiofiles
import uvicorn

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


def duration(func):
    """adapted from github: 
    https://gist.github.com/Integralist/77d73b2380e4645b564c28c53fae71fb/c2c757ff701aaf1f368a4aae232900cd846b425e#file-python-asyncio-timing-decorator-py
    """

    async def helper(func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            print(f"this function is a coroutine: {func.__name__}")
            return await func(*args, **kwargs)
        else:
            print(f"not a coroutine: {func.__name__}")
            return func(*args, **kwargs)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_ts = time.time()
        result = await helper(func, *args, **kwargs)
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))

        return result

    return wrapper


app = FastAPI()


@app.get("/hello")
@duration
def slow_hello(sleep_time: float = .5):
    """ normal function using a flexible decorator """

    print("normal function sleeping for:", sleep_time)
    time.sleep(sleep_time)
    print("normal waited")
    return {"message": "slow hello"}


@app.get("/async_hello")
@duration
async def slow_async_hello(sleep_time: float = .75):
    """ coroutine function using a flexible decorator """

    print("coroutine sleeping for:", sleep_time)
    await asyncio.sleep(sleep_time)
    print('coroutine waited')
    return {"message": "slow async hello"}


@app.get("/exception_async")
@duration
async def exception_async():
    """ coroutine function try/catch example """

    print("we're about to throw an exception")
    try:
        raise TypeError
    except TypeError:
        print("we raised an exception")
        await asyncio.sleep(.25)
    return {"message": "we got through the try/except"}


@app.get("/exception")
@duration
def exception():
    """ normal function try/catch example """

    print("we're about to throw an exception from a normal method")
    try:
        raise ValueError
    except ValueError:
        print("we raised an exception")
        time.sleep(.25)
    return {"message": "we got through the try/except"}


@app.get("/with_async")
@duration
async def with_method_async():
    """ coroutine function using with block """

    async def gen():
        async with aiofiles.open(f"{__file__}") as f:
            print("we are inside a with block")
            async for line in f:
                yield line

    return StreamingResponse(gen())


@app.get("/with")
@duration
def with_method():
    """ normal function using with block """

    print("normal function with block")

    def gen():
        with open(f"{__file__}") as f:
            # this doesn't get printed to console until the end
            print("we are inside a with block")
            for line in f:
                yield line

    return StreamingResponse(gen())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
