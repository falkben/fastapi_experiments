from fastapi.testclient import TestClient

from experiments.basic import app

client = TestClient(app)


def test_fail():
    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/fail")
    assert resp.status_code == 500
