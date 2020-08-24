import pytest
from fastapi.testclient import TestClient

from experiments.context_manager import app

client = TestClient(app)


@pytest.mark.parametrize(
    "endpoint", ["stream_context_mngr", "stream_dep", "direct_context_mngr"]
)
def test_context_mngr(endpoint):
    max_lines = 10 ** 3
    i = 0

    resp = client.get(f"/{endpoint}?iterations={max_lines}")
    assert resp.status_code == 200
    for line in resp.text.splitlines():
        if i > max_lines:
            break
        assert line == str(i)
        i += 1


@pytest.mark.parametrize(
    "endpoint", ["file_context_mngr_stream", "file_context_mngr_direct"]
)
def test_file_context_mngr(endpoint):
    """ file_context_mngr_stream test fails because the file gets closed """
    resp = client.get(endpoint)
    assert resp.status_code == 200
    assert endpoint in resp.text
