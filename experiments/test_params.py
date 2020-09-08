import pytest
from fastapi.testclient import TestClient

from experiments.params import app

client = TestClient(app)


def test_hello():
    resp = client.get("/hello?sleep_time=45")
    assert resp.status_code == 200
    assert resp.json() == {"sleep_time": "45"}


@pytest.mark.parametrize("param", ["+1.2", 1.2])
def test_float(param):
    resp = client.get(f"/float?float_p={param}")
    assert resp.status_code == 200
    assert resp.json() == float(param)


def test_fail():
    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/fail")
    assert resp.status_code == 500
