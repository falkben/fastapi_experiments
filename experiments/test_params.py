from fastapi.testclient import TestClient

from experiments.params import app

client = TestClient(app)


def test_hello():
    resp = client.get("/hello?sleep_time=45")
    assert resp.status_code == 200
    assert resp.json() == {"sleep_time": "45"}
