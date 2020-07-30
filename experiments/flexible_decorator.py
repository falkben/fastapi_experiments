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


def duration2(func):
    """
    decorator that can take either coroutine or normal function 
    works on FastAPI methods as well
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_ts = time.time()
        result = func(*args, **kwargs)
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_ts = time.time()
        result = await func(*args, **kwargs)
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return wrapper


@duration2
def main(sleep_time=.5):
    print("normal function sleeps for:", sleep_time)
    time.sleep(sleep_time)
    print('normal waited')
    return


@duration2
async def main_async(sleep_time=.75):
    print("coroutine sleeps for:", sleep_time)
    await asyncio.sleep(sleep_time)
    print('coroutine waited')
    return

if __name__ == "__main__":

    main()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async())

    print("finished")
