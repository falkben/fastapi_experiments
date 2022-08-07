import pytest

from fastapi.testclient import TestClient
from experiments.class_depends import app

client = TestClient(app)


def test_hello_class_attr():
    resp = client.get("/class_attr")
    assert resp.status_code == 200
    assert resp.json() == "hello"


def test_init_attr():
    resp = client.get("/init_attr")
    assert resp.status_code == 200
    assert resp.json() == 10


@pytest.mark.xfail
def test_class_method_depends():
    """does not work"""
    resp = client.get("/class_method_depends?names=bob&names=joe")
    assert resp.status_code == 200
    assert resp.json() == "hello bob, joe"


def test_class_method_and_depends():
    resp = client.get("/class_method_and_depends?names=bob&names=joe")
    assert resp.status_code == 200
    assert resp.json() == "hello bob, joe"
