from fastapi.testclient import TestClient

from experiments.form_json_body import app

client = TestClient(app)

data = {"name": "bob", "greeting": "hi"}


def test_form():
    resp = client.post("/form", data=data)
    assert resp.status_code == 200
    assert resp.json() == data


def test_json():
    resp = client.post("/json", json=data)
    assert resp.status_code == 200
    assert resp.json() == data
