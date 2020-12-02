from fastapi.testclient import TestClient

from experiments.form_json_body import app

client = TestClient(app)

data = {"name": "bob", "greeting": "hi"}


def test_form():
    resp = client.post("/form", json=data)
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/json"

    resp = client.post("/form", json=data, allow_redirects=True)
    assert resp.status_code == 200
    assert resp.json() == data

    resp = client.post("/form", data=data)
    assert resp.status_code == 200
    assert resp.json() == data


def test_json():
    resp = client.post("/json", json=data)
    assert resp.status_code == 200
    assert resp.json() == data
