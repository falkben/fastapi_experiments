import time
from time import sleep

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

