from fastapi.testclient import TestClient

from experiments.form_json_body import app

client = TestClient(app)

data = {"name": "bob", "greeting": "hi"}


def assert_good_response(resp):
    assert resp.status_code == 200
    assert resp.json() == data


def test_form():
    resp = client.post("/form", json=data)
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/json"

    resp = client.post("/form", json=data, allow_redirects=True)
    assert_good_response(resp)

    resp = client.post("/form", data=data)
    assert_good_response(resp)

    # test a basic validation error
    stripped_data = data.copy()
    stripped_data.pop("name")  # name is a required param
    resp = client.post("/form", data=stripped_data)
    assert resp.status_code == 422


def test_json():
    # test send json data to json endpoint (normal)
    resp = client.post("/json", json=data)
    assert_good_response(resp)

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
    assert_good_response(resp)


def test_query():
    # test sending form data to json endpoint, allowing redirect
    query_args = "&".join([f"{k}={v}" for k, v in data.items()])
    resp = client.get(f"/query?{query_args}")
    assert_good_response(resp)

    # validation error here
    query_args = "&".join([[f"{k}={v}" for k, v in data.items()][0]])
    resp = client.get(f"/query?{query_args}")
    assert resp.status_code == 422


# test form_to_json router
prefix = "/form_to_json"


def test_form_to_json_json():
    # test sending form data to json endpoint, check for redirect
    resp = client.post(prefix + "/json", data=data)
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/form"

    # test send json data to json endpoint (normal)
    resp = client.post(prefix + "/json", json=data)
    assert_good_response(resp)

    # test a basic data validation error
    # name is a required param
    stripped_data = {k: v for k, v in data.items() if k != "name"}
    resp = client.post(prefix + "/json", json=stripped_data)
    assert resp.status_code == 422

    # test sending form data to json endpoint, allowing redirect
    resp = client.post(prefix + "/json", data=data, allow_redirects=True)
    assert_good_response(resp)


def test_form_to_json_form():

    resp = client.post("/form", data=data)
    assert_good_response(resp)

    # test a basic validation error
    # name is a required param
    stripped_data = {k: v for k, v in data.items() if k != "name"}
    resp = client.post("/form", data=stripped_data)
    assert resp.status_code == 422

    # since the exception handler is on the app this still redirects
    resp = client.post("/form", json=data)
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/json"

    # since the exception handler is on the app this redirects and works
    resp = client.post("/form", json=data, allow_redirects=True)
    assert_good_response(resp)
