import pytest
from fastapi.testclient import TestClient

from experiments.regex_route import app

client = TestClient(app)


@pytest.mark.parametrize("route", ["/hello", "/hello/", "/"])
def test_get(route):
    """ GETs are redirected w/o a status code change """

    resp = client.get(route)
    assert resp.status_code == 200
    assert resp.json() == "hello"


@pytest.mark.parametrize("route,code", [("/hello", 200), ("/hello/", 200), ("/", 200)])
def test_post(route, code):
    """ POSTs w/ trailing slash redirects w/ 307s """

    resp = client.post(route, data="nada", allow_redirects=True)
    assert resp.status_code == code
    assert resp.json() == "hello"


@pytest.mark.parametrize("route", ["/hello_hello", "/hello_hello/"])
def test_double_decorated_post(route):
    """ without a redirect, needs mult. decorators """

    resp = client.post(route)
    assert resp.status_code == 200
    assert resp.json() == "hello"
