import pytest
from fastapi.testclient import TestClient

from experiments.list_param import app as list_param_app

client = TestClient(list_param_app)


def test_hello():
    resp = client.get("/hello_list")
    assert resp.status_code == 200
    assert resp.json() == {"message": "no names"}

    names = ["bob", "joe"]
    names_param = "&".join([f"names={n}" for n in names])
    resp = client.get(f"/hello?{names_param}")
    assert resp.status_code == 200

    expect_resp = "".join([f"Hello {n}" for n in names])
    assert resp.content.decode() == expect_resp


@pytest.mark.parametrize(
    "names_query,names_list",
    [
        ("names=bob&names=joe", ["bob", "joe"]),
        ("names=[bob,joe,fred]", ["bob", "joe", "fred"]),
        ('names=["bob","joe"]', ["bob", "joe"]),
        ("names=[Bob, Jeff]", ["Bob", "Jeff"]),
        ('names=["Bob", "Jeff"]', ["Bob", "Jeff"]),
        ("names=bob", ["bob"]),
    ],
)
def test_hello_list(names_query, names_list):
    resp = client.get(f"/hello_list?{names_query}")
    assert resp.status_code == 200
    expect_resp = "".join([f"Hello {n}" for n in names_list])
    assert resp.text == expect_resp


@pytest.mark.xfail
def test_json_list():
    names_param = '["Bob", "Jeff"]'
    resp = client.get(f"/json_list?names={names_param}")
    assert resp.status_code, resp.text
    assert resp.text == "Hello BobHello Jeff"

    # the following fails:
    names_param = '"Bob", "Jeff"'
    resp = client.get(f"/json_list?names={names_param}")
    assert resp.status_code, resp.text
    assert resp.text == "Hello BobHello Jeff"
