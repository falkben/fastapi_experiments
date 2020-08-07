import uvicorn
from fastapi import FastAPI, Request, Query

app = FastAPI()


@app.get("/hello")
def hello(request: Request, sleep_time: int = Query(None)):
    query_params = request.query_params.items()
    sleep_time
    return query_params


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
