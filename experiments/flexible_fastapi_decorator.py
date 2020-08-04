""" flexible decorator around fastapi routes
call with: `uvicorn flexible_fastapi_decorator:app --reload` or `python flexible_fastapi_decorator.py`
stackoverflow: https://stackoverflow.com/q/44169998/532963
important piece seems to be that the wrapper needs to be async
"""

import asyncio
import functools
import time
from contextlib import contextmanager

import aiofiles
import uvicorn

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


class SyncAsyncDecoratorFactory:
    """ This is a factory class for creating decorators that properly calls sync or async
    Override the "wrapper" function for your specific decorator
    """

    @contextmanager
    def wrapper(self, func, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            with self.wrapper(func, *args, **kwargs):
                return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            with self.wrapper(func, *args, **kwargs):
                return await func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper


class Duration(SyncAsyncDecoratorFactory):
    """ decorator using class inheritance
    """

    @contextmanager
    def wrapper(self, func, *args, **kwargs):
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print(f"{func.__name__} took {dur:.2} seconds")
        if asyncio.iscoroutinefunction(func):
            return print("async func call")
        else:
            return print("normal func call")


app = FastAPI()


@app.get("/hello")
@Duration()
def slow_hello(sleep_time: float = 0.5):
    """ normal function using a flexible decorator """

    print("normal function sleeping for:", sleep_time)
    time.sleep(sleep_time)
    print("normal waited")
    return {"message": "slow hello"}


@app.get("/async_hello")
@Duration()
async def slow_async_hello(sleep_time: float = 0.75):
    """ coroutine function using a flexible decorator """

    print("coroutine sleeping for:", sleep_time)
    await asyncio.sleep(sleep_time)
    print("coroutine waited")
    return {"message": "slow async hello"}


@app.get("/exception_async")
@Duration()
async def exception_async():
    """ coroutine function try/catch example """

    print("we're about to throw an exception")
    try:
        raise TypeError
    except TypeError:
        print("we raised an exception")
        await asyncio.sleep(0.25)
    return {"message": "we got through the try/except"}


@app.get("/exception")
@Duration()
def exception():
    """ normal function try/catch example """

    print("we're about to throw an exception from a normal method")
    try:
        raise ValueError
    except ValueError:
        print("we raised an exception")
        time.sleep(0.25)
    return {"message": "we got through the try/except"}


@app.get("/with_async")
@Duration()
async def with_method_async():
    """ coroutine function using with block """

    async def gen():
        async with aiofiles.open(f"{__file__}") as f:
            print("we are inside a with block")
            async for line in f:
                yield line

    return StreamingResponse(gen())


@app.get("/with")
@Duration()
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
