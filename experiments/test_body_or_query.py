import pytest
from fastapi.testclient import TestClient

from experiments.body_or_query import app

client = TestClient(app)


def test_body_or_query():
    data = {"p_int": 1, "p_str": "5.2", "p_float": 100}
    resp = client.post("/?p_float=4.3", json=data)
    # query args currently overwrite body data but maybe we should throw an exception
    assert resp.json() == {**data, "p_float": 4.3}

    resp = client.post("/?p_int=1&p_float=4.3&p_str=5.2")
    assert resp.json() == {"p_int": 1, "p_float": 4.3, "p_str": "5.2"}, resp.text

    data = {"p_int": 1, "p_float": 4.3, "p_str": "5.2"}
    resp = client.post("/", json=data)
    assert resp.json() == data

    data = {"p_int": 1, "p_str": "5.2"}
    resp = client.post("/?p_float=4.3", json=data)
    assert resp.json() == {**data, "p_float": 4.3}


@pytest.mark.xfail
def test_b_or_q():
    resp = client.post("/b_or_q?p_int=1&p_float=4.3&p_str=5.2")
    assert resp.json() == {"p_int": 1, "p_float": 4.3, "p_str": "5.2"}, resp.text

    data = {"p_int": 1, "p_float": 4.3, "p_str": "5.2"}
    resp = client.post("/b_or_q", json=data)
    assert resp.json() == data

    data = {"p_int": 1, "p_str": "5.2"}
    resp = client.post("/b_or_q?p_float=4.3", json=data)
    assert resp.json() == {**data, "p_float": 4.3}

    data = {"p_int": 1, "p_str": "5.2", "p_float": 100}
    resp = client.post("/b_or_q?p_float=4.3", json=data)
    # not sure how we handle both params
    assert resp.json() == {**data, "p_float": 100}
