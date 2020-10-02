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


@pytest.mark.parametrize("flag_param", [True, False, "anything", None])
def test_flag(flag_param):
    if flag_param is not None:
        resp = client.get(f"/flag?f={flag_param}")
        flag_test = True
    else:
        resp = client.get("/flag")
        flag_test = False

    assert resp.status_code == 200
    assert resp.json() == flag_test
