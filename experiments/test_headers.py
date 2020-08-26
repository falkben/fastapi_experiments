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
