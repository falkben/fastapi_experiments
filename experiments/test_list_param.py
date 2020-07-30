from fastapi.testclient import TestClient
from experiments.list_param import app as list_param_app


client = TestClient(list_param_app)


def test_hello():
    resp = client.get('/hello_list')
    assert resp.status_code == 200
    assert resp.json() == {"message": "no names"}


def test_hello_list():
    names = ["bob", "joe"]
    names_param = "&".join([f"names={n}" for n in names])
    resp = client.get(f'/hello?{names_param}')
    assert resp.status_code == 200

    expect_resp = "".join([f"Hello {n}" for n in names])
    assert resp.content.decode() == expect_resp


def test_hello_names():
    names = ["bob", "joe"]
    names_param = "&".join([f"names={n}" for n in names])
    resp = client.get(f'/hello_list?{names_param}')
    assert resp.status_code == 200

    expect_resp = "".join([f"Hello {n}" for n in names])
    assert resp.content.decode() == expect_resp


def test_hello_names_list():
    names = ["bob", "joe", "fred"]
    names_param = f"[{','.join(names)}]"
    resp = client.get(f'/hello_list?names={names_param}')
    assert resp.status_code == 200

    expect_resp = "".join([f"Hello {n}" for n in names])
    assert resp.content.decode() == expect_resp


def test_hello_names_with_quotes():
    names = ["bob", "joe"]
    names_bracket_wrap = "\",\"".join(names)
    names_param = f"[\"{names_bracket_wrap}\"]"
    resp = client.get(f'/hello_list?names={names_param}')
    assert resp.status_code == 200

    expect_resp = "".join([f"Hello {n}" for n in names])
    assert resp.content.decode() == expect_resp


def test_hello_names_spaces():
    names_param = '[Bob, Jeff]'
    resp = client.get(f'/hello_list?names={names_param}')
    assert resp.status_code == 200
    expect_resp = "Hello BobHello Jeff"
    assert resp.content.decode() == expect_resp


def test_hello_names_spaces_quotes():
    names_param = '["Bob", "Jeff"]'
    resp = client.get(f'/hello_list?names={names_param}')
    assert resp.status_code == 200
    expect_resp = "Hello BobHello Jeff"
    assert resp.content.decode() == expect_resp
