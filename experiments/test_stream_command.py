"""Tests for stream_command.py"""
import asyncio
import itertools

import httpx
import pytest
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from experiments.stream_command import stream_command_async

stream_yes = FastAPI()


@stream_yes.get("/stream_yes")
async def get_stream_yes():
    """
    Run the yes command and stream results. Yes runs forever so this should be an
    infinite stream.
    """
    cmd = ["yes"]
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
    stream_gen = stream_command_async(proc)
    return StreamingResponse(stream_gen)


@stream_yes.get("/stream_yes_fake")
async def get_stream_yes_fake():
    """
    Returns an infinite stream of "y"
    """
    y_gen = itertools.repeat("y\n")
    return StreamingResponse(y_gen)


""" Tests
To run without captured output use pytest -s experiments/test_stream_command.py
"""


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()

    yield loop
    # If we close the loop here or use the default event_loop fixture, which also gets closed,
    # we get a bunch of errors about pending Tasks.
    # loop.close()


# This is an example of how we would set up a test with httpx, but it currently doesn't work
@pytest.mark.skip("This test hangs forever")
@pytest.mark.asyncio
async def test_stream_yes_httpx():
    print("testing yes")
    max_lines = 1000
    i = 0
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        # It seems that the AsyncClient.stream does not work asynchronously
        async with aclient.stream("GET", "/stream_yes") as response:
            async for line in response.aiter_lines():
                if i > max_lines:
                    break
                assert line.strip() == "n"
                i += 1


# Note that the test failing has nothing to do with the subprocess call. This fake version also fails.
@pytest.mark.skip("This test hangs forever")
@pytest.mark.asyncio
async def test_stream_yes_fake_httpx():
    max_lines = 1000
    i = 0
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        async with aclient.stream("GET", "/stream_yes_fake") as response:
            async for line in response.aiter_lines():
                if i > max_lines:
                    break
                assert line.strip() == "y"
                i += 1


@pytest.mark.asyncio
async def test_stream_yes():
    """Get the first 1000 lines from the infinite stream and test that the output is always 'y' """
    max_lines = 1000
    i = 0
    async with TestClient(stream_yes) as client:
        response = await client.get("/stream_yes", stream=True)
        async for line in response.iter_content(2):
            if i > max_lines:
                break
            line = line.decode("utf-8").strip()
            assert line == "y"
            i += 1


if __name__ == "__main__":
    # Run `uvicorn experiments.test_stream_command:stream_yes`
    # Then python experiemtns/test_stream_comman.py

    # Note that we can fetch with the httpx client from the stream_yes app running in uvicorn
    async def fetch_stream():
        max_lines = 1000
        i = 0
        async with httpx.AsyncClient() as aclient:
            async with aclient.stream("GET", "http://localhost:8000/stream_yes") as r:
                async for line in r.aiter_lines():
                    if i > max_lines:
                        break
                    print(line.strip())
                    i += 1

    def sync_fetch_stream():
        max_lines = 1000
        i = 0
        with httpx.Client() as client:
            with client.stream("GET", "http://localhost:8000/stream_yes") as response:
                for line in response.iter_lines():
                    if i > max_lines:
                        break
                    print(line.strip())
                    i += 1

    sync_fetch_stream()

    # We could run this using an async client, but we don't have to
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(fetch_stream())
