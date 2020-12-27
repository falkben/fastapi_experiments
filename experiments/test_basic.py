import pytest
from async_asgi_testclient import TestClient as AsyncTestClient
from fastapi.testclient import TestClient

from experiments.basic import app

client = TestClient(app)


def test_fail():
    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/fail")
    assert resp.status_code == 500


@pytest.mark.asyncio
async def test_async_fail():
    async with AsyncTestClient(app) as client:
        resp = await client.get("/fail")
        assert resp.status_code == 500
