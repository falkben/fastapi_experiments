from fastapi.testclient import TestClient

from experiments.form_list import app

client = TestClient(app)


def test_hello():
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.json() == "hello"


def test_hello_params():
    resp = client.get("/hello", data=[("params", "a"), ("params", "b")])
    assert resp.status_code == 200
    assert resp.json() == ["a", "b"]


def test_hello_post():
    resp = client.post("/hello")
    assert resp.status_code == 200
    assert resp.json() == "hello"


def test_hello_post_params():
    resp = client.post("/hello", data=[("params", "a"), ("params", "b")])
    assert resp.status_code == 200
    assert resp.json() == ["a", "b"]
