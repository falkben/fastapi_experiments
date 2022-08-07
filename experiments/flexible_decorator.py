import asyncio
import functools
import time
from contextlib import contextmanager

"""
from stackoverflow: https://stackoverflow.com/q/44169998/532963
"""


def duration(func):
    """decorator that can take either coroutine or normal function
    I cannot get this to work w/ FastAPI async methods
    """

    @contextmanager
    def wrapping_logic():
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print("{} took {:.2} seconds".format(func.__name__, dur))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def sync_wrapper(func, *args, **kwargs):
            with wrapping_logic():
                return func(*args, **kwargs)

        async def async_wrapper(func, *args, **kwargs):
            with wrapping_logic():
                return await func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper(func, *args, **kwargs)
        else:
            return sync_wrapper(func, *args, **kwargs)

    return wrapper


class SyncAsyncDecoratorFactory:
    """Using class inheritance to abstract the wrapper and repeat as little as possible"""

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


class duration3(SyncAsyncDecoratorFactory):
    """decorator using class inheritance"""

    @contextmanager
    def wrapper(self, func, *args, **kwargs):
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print(f"{func.__name__} took {dur:.2} seconds")


@duration
def main(sleep_time=0.5):
    print("normal function sleeps for:", sleep_time)
    time.sleep(sleep_time)
    print("normal waited")
    return


@duration
async def main_async(sleep_time=0.75):
    print("coroutine sleeps for:", sleep_time)
    await asyncio.sleep(sleep_time)
    print("coroutine waited")
    return


if __name__ == "__main__":

    main()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async())

    print("finished")
