import uvicorn
from fastapi import FastAPI, Query, Request

app = FastAPI()


@app.get("/hello")
def hello(request: Request, sleep_time: int = Query(None)):
    """ Can get query args not defined as params """
    query_params = request.query_params.items()
    return query_params


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
