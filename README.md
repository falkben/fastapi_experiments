# Short experiments in FastAPI

Each experiment should be runnable as a single file, which allows convenient debugging from within vscode:

`python experiments/FILENAME.py`

When making frequent changes to the file and you want to immediately see the changes, you can run:

`uvicorn experiments.FILENAME:app --reload`

## Install

Create a virtual environment, activate, then:

`pip install -e .`

## Boilerplate

App:

```py
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# experiment path operators here
@app.get("/hello")
async def hello():
    return "hello"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Test file:

```py
from fastapi.testclient import TestClient

from experiments.FILENAME import app

client = TestClient(app)


# TEST path operators here
def test_hello():
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.json() == "hello"
```
