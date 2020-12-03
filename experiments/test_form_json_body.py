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

    # test a basic validation error
    stripped_data = data.copy()
    stripped_data.pop("name")  # name is a required param
    resp = client.post("/form", data=stripped_data)
    assert resp.status_code == 422


def test_json():
    # test send json data to json endpoint (normal)
    resp = client.post("/json", json=data)
    assert resp.status_code == 200
    assert resp.json() == data

    # test a basic data validation error
    stripped_data = data.copy()
    stripped_data.pop("name")  # name is a required param
    resp = client.post("/json", json=stripped_data)
    assert resp.status_code == 422

    # test sending form data to json endpoint, check for redirect
    resp = client.post("/json", data=data)
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/form"

    # test sending form data to json endpoint, allowing redirect
    resp = client.post("/json", data=data, allow_redirects=True)
    assert resp.status_code == 200
    assert resp.json() == data


def test_query():
    # test sending form data to json endpoint, allowing redirect
    query_args = "&".join([f"{k}={v}" for k, v in data.items()])
    resp = client.get(f"/query?{query_args}")
    assert resp.status_code == 200
    assert resp.json() == data

    # validation error here
    query_args = "&".join([[f"{k}={v}" for k, v in data.items()][0]])
    resp = client.get(f"/query?{query_args}")
    assert resp.status_code == 422
