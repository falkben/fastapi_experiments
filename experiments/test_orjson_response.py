import time
from datetime import datetime

from fastapi.testclient import TestClient

from experiments.orjson_response import app

client = TestClient(app)

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def measure_endpoint(route):
    t0 = time.time()
    for _ in range(100):
        client.get(route)
    t1 = time.time()
    print(f"{route}, {(t1 - t0):0.3f}s")
    resp = client.get(route)
    data = resp.json()
    right_now = datetime.now()
    date_data = datetime.strptime(data["results"]["dates"][0], DATETIME_FORMAT)
    assert right_now > date_data


def test_orjson():
    print("\n")
    measure_endpoint("/a")
    measure_endpoint("/b")
    measure_endpoint("/c")
    measure_endpoint("/d")
    measure_endpoint("/e")
    measure_endpoint("/f")
    measure_endpoint("/g")


# output
# /a, 7.029s
# /b, 1.148s
# /c, 1.157s
# /d, 1.181s
# /e, 1.163s
# /f, 1.152s
# /g, 1.547s

if __name__ == "__main__":
    test_orjson()
