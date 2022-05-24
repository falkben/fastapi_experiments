from typing import List, Optional

import uvicorn
from fastapi import APIRouter, Body, FastAPI, Query
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.post("/post")
def post(names: List[str] = Body(..., embed=True)):
    query_names = "&".join([f"names={name}" for name in names])
    return RedirectResponse(url=f"/get?{query_names}", status_code=303)


@router.get("/get")
def get(names: Optional[List[str]] = Query(None, description="list of names")):
    return names


app = FastAPI()
app.include_router(router)


########################################################################################

from fastapi.testclient import TestClient

client = TestClient(app)


def test_post_redirect():
    response = client.post("/post", json={"names": ["a", "b"]}, allow_redirects=True)
    assert response.status_code == 200
    assert response.json() == ["a", "b"]


def test_post_no_redirect():
    response = client.post("/post", json={"names": ["a", "b"]}, allow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/get?names=a&names=b"


########################################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
