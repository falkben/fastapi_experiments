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


def test_animal():
    resp = client.get("/animal")
    assert resp.status_code == 200

    resp = client.get("/animal?anim=CAT")
    assert resp.status_code == 200
    assert resp.json() == "CAT"

    resp = client.get("/animal?anim=cat")
    # case sensitive, if not in enum then we return an error and method doesn't run
    assert resp.status_code == 422
