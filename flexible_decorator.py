import asyncio
import functools
import time
from contextlib import contextmanager


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


@duration
def main(sleep_time):
    time.sleep(sleep_time)
    return


@duration
async def main_async(sleep_time):
    asyncio.sleep(sleep_time)
    return

if __name__ == "__main__":

    sleep_time = 0.5
    print("normal function sleeps for:", sleep_time)
    main(sleep_time)

    sleep_time_async = 0.75
    print("coroutine sleeps for:", sleep_time_async)
    main_async(sleep_time_async)
