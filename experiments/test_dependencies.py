from fastapi.testclient import TestClient

from experiments.dependencies import app

client = TestClient(app)


def test_items():
    resp = client.get("/items")
    assert resp.status_code == 200
