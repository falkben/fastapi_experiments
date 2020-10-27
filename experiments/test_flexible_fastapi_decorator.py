import time

from fastapi.testclient import TestClient

from experiments.flexible_fastapi_decorator import app

client = TestClient(app)


def test_hello():
    sleep_time = 0.25
    start_ts = time.time()
    resp = client.get(f"/hello?sleep_time={sleep_time}")
    dur = time.time() - start_ts
    assert resp.status_code == 200
    assert resp.json() == {"message": "slow hello"}
    assert dur > sleep_time


def test_async_hello():
    sleep_time = 0.25
    start_ts = time.time()
    resp = client.get(f"/async_hello?sleep_time={sleep_time}")
    dur = time.time() - start_ts
    assert resp.status_code == 200
    assert resp.json() == {"message": "slow async hello"}
    assert dur > sleep_time


def test_redirect():
    # this has the decorator but disables the redirect location
    resp = client.get("/no_redirect")
    assert resp.status_code == 200
    assert resp.json() == {"message": "hello"}

    for endpoint in ["/redirect", "/redirect_async"]:
        resp = client.get(endpoint, allow_redirects=True)
        assert resp.status_code == 200
        assert resp.json() == {"message": "bye"}


def test_redirect_cbv():

    for endpoint in ["/cbv/hello", "/cbv/hello_async"]:
        resp = client.get(endpoint)
        assert resp.status_code == 200
        assert resp.json() == {"message": "bye"}


def test_modify_attr():
    resp = client.get("/cbv/no_class_attr")
    assert resp.status_code == 200
    assert resp.json() == {"value": 2}

    resp = client.get("/cbv/no_dec_value_class_attr")
    assert resp.status_code == 200
    assert resp.json() == {"value": None}

    resp = client.get("/cbv/modify_attr?value=0")
    assert resp.status_code == 200
    assert resp.json() == {"value": 0}

    resp = client.get("/cbv/modify_attr")
    assert resp.status_code == 200
    assert resp.json() == {"value": 1}
