from fastapi.testclient import TestClient

from experiments.headers import app

client = TestClient(app)


# TEST path operators here
def test_hello():
    resp = client.get("/hello")
    assert resp.status_code == 200
    # this works even though we have a different "case"
    # because resp. headers is of type: requests.structures.CaseInsensitiveDict
    assert "Content-Security-Policy" in resp.headers
    assert resp.headers["Content-Security-Policy"] == "default-src 'self'"


def test_accept_header():
    resp = client.get("accept")
    assert resp.status_code == 200
    # returns json
    assert resp.headers["Content-Type"] == "application/json"

    resp = client.get("accept", headers={"Accept": "text/html"})
    assert resp.status_code == 200
    assert resp.json()["accept"] == "text/html"


def test_accept_custom():
    resp = client.get("accept_custom")
    assert resp.status_code == 200
    # default to json
    assert resp.headers["Content-Type"] == "application/json"

    resp = client.get("accept_custom", headers={"Accept": "text/html"})
    assert resp.status_code == 200
    assert resp.json()["accept"] == "text/html"
    assert "text/html; charset=utf-8" in resp.headers["Content-Type"]


def test_accept_stream():
    resp = client.get("accept_stream")
    assert resp.status_code == 200
    # default to json
    assert resp.headers["Content-Type"] == "application/json"

    resp = client.get("accept_stream", headers={"Accept": "text/html"})
    assert resp.status_code == 200
    assert resp.json()["accept"] == "text/html"
    assert "text/html; charset=utf-8" in resp.headers["Content-Type"]


def test_file_stream():
    resp = client.get("file_stream")
    assert resp.status_code == 200
    assert "Content-Disposition" in resp.headers
