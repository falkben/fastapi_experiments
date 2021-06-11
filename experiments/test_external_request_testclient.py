import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/redirector")
async def redirector():
    return RedirectResponse("https://docs.python.org/")


client = TestClient(app)


def test_redirector():
    resp = client.get("/redirector", allow_redirects=True)
    # returns a 404 instead of 200
    assert resp.status_code == 404


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
