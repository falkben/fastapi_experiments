from fastapi.testclient import TestClient

from experiments.enumerate_params import app

client = TestClient(app)


def test_hello():
    resp = client.get("/hello?first_name=bob")
    assert resp.status_code == 200
    assert resp.json() == "hello bob"

    resp = client.get("/hello?first_name=doug")
    assert resp.status_code == 200
    assert resp.json() == "hello doug"

    resp = client.get("/hello?first_name=josh")
    assert resp.status_code == 422

    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.json() == "hello "
