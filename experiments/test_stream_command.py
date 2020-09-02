"""Tests for stream_command.py"""
import pytest
import httpx
import asyncio
from experiments.stream_command import stream_yes

# To run without captured output use pytest -s experiments/test_stream_command.py

@pytest.mark.skip("This test doesn't work")
@pytest.mark.asyncio
async def test_streaming_command_yes():
    print("testing yes")
    max_lines = 1000
    i = 0
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        async with aclient.stream("GET", "/stream_yes") as response:
            async for line in response.aiter_lines():
                if i > max_lines:
                    break
                assert line.strip() == "n"
                print(line.strip())
                i += 1


async def _helper():
    max_lines = 1000
    i = 0
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        async with aclient.stream("GET", "/stream_yes_fake") as response:
            async for line in response.aiter_lines():
                if i > max_lines:
                    break
                assert line.strip() == "n"
                print(line.strip())
                i += 1

@pytest.mark.asyncio
@pytest.mark.skip("This test doesn't work")
async def test_streaming_command_yes_fake_loop():
    print("testing yes fake")
    # event_loop = asyncio.get_event_loop()
    # event_loop.run_until_complete(_helper())
    task = asyncio.create_task(_helper())
    (done, pending) = await asyncio.wait({task}, return_when=asyncio.FIRST_COMPLETED)
    [task.cancel() for task in pending]
    [task.result() for task in done]

@pytest.mark.skip("This test doesn't work")
@pytest.mark.asyncio
async def test_streaming_command_yes_fake():
    max_lines = 1000
    i = 0
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        async with aclient.stream("GET", "/stream_yes_fake") as response:
            async for line in response.aiter_lines():
                if i > max_lines:
                    break
                assert line.strip() == "n"
                print(line.strip())

# Note: Tests work if we truncate the output
@pytest.mark.asyncio
async def test_streaming_command_yes_fake_truncate():
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        async with aclient.stream("GET", "/stream_yes_fake_truncate") as response:
            async for line in response.aiter_lines():
                assert line.strip() == "y"
                print(line.strip())


@pytest.mark.asyncio
async def test_streaming_command_yes_truncate():
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        async with aclient.stream("GET", "/stream_yes_truncate") as response:
            async for line in response.aiter_lines():
                assert line.strip() == "y"
                print(line.strip())


import itertools

# @pytest.mark.asyncio
# async def test_infinite_gen():
#     yes_gen = itertools.repeat("yes")
#     for val in yes_gen:
#         assert val == "yes"
#         print(val)

if __name__ == "__main__":
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

