from fastapi.testclient import TestClient

from experiments.params import app

client = TestClient(app)


def test_hello():
    resp = client.get(f"/hello?sleep_time=45")
    assert resp.status_code == 200
    assert resp.json() == {"sleep_time": "45"}


def test_conv():
    resp = client.get(f"/conv?p_int=1&p_float=4.3&p_str=5.2")

    assert resp.json() == {"p_int": 1, "p_float": 4.3, "p_str": "5.2"}


def test_conv_post():
    data = {"p_int": 1, "p_float": 4.3, "p_str": "5.2"}
    resp = client.post("/conv", json=data)

    assert resp.json() == data


def test_conv_post_and_query():
    data = {"p_int": 1, "p_str": "5.2"}
    resp = client.post("/conv?p_float=4.3", json=data)

    assert resp.json() == {**data, "p_float": 4.3}

