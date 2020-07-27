"""
start with:
uvicorn test_streaming_response:app --reload
"""

import asyncio
import time

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


def infinite_generator():
    # not blocking, so doesn't need to be async
    # but if it was blocking, you could make this async and await it
    while True:
        yield b"some fake data "


def finite_generator():
    # not blocking, so doesn't need to be async
    # but if it was blocking, you could make this async and await it
    x = 0
    while x < 3000:
        yield f"{x}"
        x += 1


async def astreamer(generator):
    try:
        # if it was an async generator we'd do:
        # "async for data in generator:"
        # (there is no "yield from" for async generators)
        for i in generator:
            yield i
            await asyncio.sleep(.001)

    except asyncio.CancelledError as e:
        print('cancelled')


def streamer(generator):
    try:
        # note: normally we would do "yield from generator"
        # but that won't work with next(generator) in the finally statement
        for i in generator:
            yield i
            time.sleep(.001)

    except GeneratorExit:
        print("cancelled")
    finally:
        # showing that we can check here to see if all data was consumed
        # the except statement above effectively does the same thing
        try:
            next(generator)
            print("we didn't finish")
            return
        except StopIteration:
            print("we finished")


@app.get("/infinite")
async def infinite_stream():
    return StreamingResponse(streamer(infinite_generator()))


@app.get("/finite")
async def finite_stream():
    return StreamingResponse(streamer(finite_generator()))


@app.get("/ainfinite")
async def infinite_stream():
    return StreamingResponse(astreamer(infinite_generator()))


@app.get("/afinite")
async def finite_stream():
    return StreamingResponse(astreamer(finite_generator()))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
