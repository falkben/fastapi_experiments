# Short experiments in FastAPI

Each experiment should be runnable as a single file, which allows convenient debugging from within vscode:

`python experiments/FILENAME.py`

When making frequent changes to the file and you want to immediately see the changes, you can run:

`uvicorn experiments.FILENAME:app --reload`

## Install

Create a virtual environment, activate, then:

```cmd
pip install -r requirements.txt -e .
```

## Dependencies

Use pip-tools (`pip install pip-tools`)

`pip-compile --quiet --upgrade` to upgrade lock file

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
    uvicorn.run(app, host="localhost", port=8000)
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

## pre-commit

To install and ensure it's working, run:

```cmd
pre-commit install
pre-commit run --all-files
```
