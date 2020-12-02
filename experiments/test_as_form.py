from fastapi.testclient import TestClient

from experiments.as_form import app

client = TestClient(app)

data = {
    "client_id": "1",
    "state": "1232",
    "scope": "all",
    "redirect_url": "some_url",
    "redirect_uri": "some_uri",
}


def test_form():
    pop_data = data.copy()
    pop_data.pop("state")
    query_data = data.get("state")
    resp = client.post(f"/query-form?state={query_data}", data=pop_data)
    assert resp.status_code == 200
    assert resp.json() == data

    resp = client.post("/query-form", data=data)
    assert resp.status_code == 200
    assert resp.json() == data


def test_json():
    pop_data = data.copy()
    pop_data.pop("state")
    query_data = data.get("state")
    resp = client.post(f"/query-json?state={query_data}", json=pop_data)
    assert resp.status_code == 200
    assert resp.json() == data

    resp = client.post("/query-json", json=data)
    assert resp.status_code == 200
    assert resp.json() == data
