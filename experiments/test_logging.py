from fastapi.testclient import TestClient

from experiments.logger import app

client = TestClient(app)


def test_hello():
    resp = client.get("/hello")
    assert resp.status_code == 200


def test_bad_route():
    resp = client.get("/bad_route")
    assert resp.status_code == 500
