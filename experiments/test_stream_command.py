"""Tests for stream_command.py"""
import pytest
import httpx

from experiments.stream_command import stream_yes

# To run without captured output use pytest -s experiments/test_stream_command.py

# @pytest.mark.skip("This test doesn't work")
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
                assert line.strip() == "y"
                print(line.strip())
                i += 1


@pytest.mark.skip("This test doesn't work")
@pytest.mark.asyncio
async def test_streaming_command_yes_fake():
    print("testing yes fake")
    max_lines = 1000
    i = 0
    async with httpx.AsyncClient(app=stream_yes, base_url="http://test") as aclient:
        async with aclient.stream("GET", "/stream_yes_fake") as response:
            async for line in response.aiter_lines():
                if i > max_lines:
                    break
                assert line.strip() == "y"
                print(line.strip())
                i += 1


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

