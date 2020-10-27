""" flexible decorator around fastapi routes
call with: `uvicorn flexible_fastapi_decorator:app --reload` or
`python flexible_fastapi_decorator.py`
stackoverflow: https://stackoverflow.com/q/44169998/532963
"""

import asyncio
import functools
import inspect
import time
from contextlib import contextmanager
from typing import Optional

import aiofiles
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi_utils.cbv import cbv


class SyncAsyncDecoratorFactory:
    """ This is a factory class for creating decorators that properly calls sync or async
    Override the "wrapper" function for your specific decorator
    To return something from wrapper use self._return
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        # This is for using decorator without parameters
        if (
            len(args) == 1
            and not kwargs
            and (inspect.iscoroutinefunction(args[0]) or inspect.isfunction(args[0]))
        ):
            instance.__init__()
            return instance(args[0])
        return instance

    @contextmanager
    def wrapper(self, *args, **kwargs):
        raise NotImplementedError

    class ReturnValue(Exception):
        def __init__(self, return_value):
            self.return_value = return_value

    @classmethod
    def _return(cls, value):
        """ this can be used to exit the context manager
        returns whatever is in value
        """
        raise cls.ReturnValue(value)

    def __call__(self, func):
        @functools.wraps(func)
        def call_sync(*args, **kwargs):
            try:
                with self.wrapper(*args, **kwargs) as new_args:
                    if new_args:
                        args, kwargs = new_args
                    return self.func(*args, **kwargs)
            except self.ReturnValue as r:
                return r.return_value

        @functools.wraps(func)
        async def call_async(*args, **kwargs):
            try:
                with self.wrapper(*args, **kwargs) as new_args:
                    if new_args:
                        args, kwargs = new_args
                    return await self.func(*args, **kwargs)
            except self.ReturnValue as r:
                return r.return_value

        self.func = func
        return call_async if inspect.iscoroutinefunction(func) else call_sync


class Duration(SyncAsyncDecoratorFactory):
    """ decorator using class inheritance
    """

    def __init__(self, default=None):
        self.default_value = default

    @contextmanager
    def wrapper(self, *args, **kwargs):
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print(f"{self.func.__name__} took {dur:.2} seconds")
        print(f"some default value: {self.default_value}")
        if asyncio.iscoroutinefunction(self.func):
            return print("async func call")
        else:
            return print("normal func call")


class RedirectTo(SyncAsyncDecoratorFactory):
    """ decorator using class inheritance
    """

    def __init__(self, location=None):
        self.location = location

    @contextmanager
    def wrapper(self, *args, **kwargs):
        if self.location is None:
            yield
        else:
            self._return(RedirectResponse(self.location))


class CVBRedirectTo(SyncAsyncDecoratorFactory):
    """ decorator using class inheritance
    Can accesses instance variables (self is passed in as a kwarg so need a new var name for that)
    """

    def __init__(self, location=None):
        self.location = location

    @contextmanager
    def wrapper(dec_self, *args, self=None, **kwargs):

        if self:
            print("self.one", self.one)

        if dec_self.location is None:
            yield
        else:
            dec_self._return(RedirectResponse(dec_self.location))


app = FastAPI()
router = APIRouter()


@cbv(router)
class HelloClass:
    def __init__(self):
        self.one = 1

    @router.get("/hello")
    @CVBRedirectTo(location="/goodbye")
    def cbv_hello(self):
        return {"message": "hello"}

    @router.get("/hello_async")
    @CVBRedirectTo(location="/goodbye")
    async def cbv_hello_async(self):
        return {"message": "hello"}


@app.get("/hello")
@Duration
def slow_hello(sleep_time: float = 0.5):
    """ normal function using a flexible decorator """

    print("normal function sleeping for:", sleep_time)
    time.sleep(sleep_time)
    print("normal waited")
    return {"message": "slow hello"}


@app.get("/async_hello")
@Duration(default=100)
async def slow_async_hello(sleep_time: float = 0.75):
    """ coroutine function using a flexible decorator """

    print("coroutine sleeping for:", sleep_time)
    await asyncio.sleep(sleep_time)
    print("coroutine waited")
    return {"message": "slow async hello"}


@app.get("/no_redirect")
@RedirectTo
async def no_redirect():
    return {"message": "hello"}


@app.get("/redirect_async")
@CVBRedirectTo(location="/goodbye")
async def redirect_async():
    return {"message": "hello"}


@app.get("/redirect")
@RedirectTo(location="/goodbye")
def redirect():
    return {"message": "hello"}


@app.get("/goodbye")
async def goodbye():
    return {"message": "bye"}


@app.get("/exception_async")
@Duration
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
@Duration
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
@Duration
async def with_method_async():
    """ coroutine function using with block """

    async def gen():
        async with aiofiles.open(f"{__file__}") as f:
            print("we are inside a with block")
            async for line in f:
                yield line

    return StreamingResponse(gen())


@app.get("/with")
@Duration
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


class DecoratModifyAttr(SyncAsyncDecoratorFactory):
    """ example showing yield of data back to func
    """

    def __init__(self, value=None):
        self.value = value

    @contextmanager
    def wrapper(dec_self, *args, self=None, **kwargs):

        # if there's no value arg specified by user
        if kwargs.get("value") is None:
            # we first set it to the decorated class' value
            if hasattr(self, "value") and self.value:
                yield (self,), {"value": self.value}
            # if that doesn't exist, we override it with the decorator value
            elif dec_self.value:
                yield (self,), {"value": dec_self.value}
            else:
                yield
        else:
            yield


@cbv(router)
class ClassWithAttr:
    def __init__(self):
        self.value = 1

    @router.get("/modify_attr")
    @DecoratModifyAttr(value=2)
    def modify_attr(self, value: Optional[int] = None):
        return {"value": value}


@cbv(router)
class ClassWithOutAttr:
    @router.get("/no_class_attr")
    @DecoratModifyAttr(value=2)
    def no_class_attr(self, value: Optional[int] = None):
        return {"value": value}

    @router.get("/no_dec_value_class_attr")
    @DecoratModifyAttr
    def no_dec_value_class_attr(self, value: Optional[int] = None):
        return {"value": value}


app.include_router(router, prefix="/cbv")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
