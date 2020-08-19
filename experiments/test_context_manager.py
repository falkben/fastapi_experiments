from fastapi.testclient import TestClient

from experiments.context_manager import app

client = TestClient(app)


def test_hello():
    max_lines = 10 ** 3
    i = 0

    resp = client.get("/hello")
    assert resp.status_code == 200
    for line in resp.text.splitlines():
        if i > max_lines:
            break
        assert line == "hello"
        i += 1


def test_hello_dep():
    max_lines = 10 ** 3
    i = 0

    resp = client.get("/hello_dep")
    assert resp.status_code == 200
    for line in resp.text.splitlines():
        if i > max_lines:
            break
        assert line == "hello"
        i += 1
