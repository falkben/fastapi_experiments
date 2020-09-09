import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/fail")
def failing_endpoint():
    # pyright: reportUndefinedVariable=false
    return not_exist  # noqa: F821


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
