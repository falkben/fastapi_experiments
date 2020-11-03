import logging
import sys
import time

import uvicorn
from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi_utils.cbv import cbv

app = FastAPI()

base_logger = logging.getLogger(__name__)
base_logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

base_logger.addHandler(handler)


def request_summary(request):
    return f"{request.method} {request.url.path} ({request.client.host})"


@app.middleware("http")
async def log_all(request: Request, call_next):

    start_time = time.perf_counter()
    resp = await call_next(request)
    request_time = (time.perf_counter() - start_time) * 1000.0

    rlog = base_logger
    if hasattr(request.state, "log"):
        rlog = request.state.log

    if resp.status_code < 400:
        log_method = rlog.info
    elif resp.status_code < 500:
        log_method = rlog.warning
    else:
        log_method = rlog.error

    log_method(f"{resp.status_code} {request_summary(request)} {request_time:.2f}ms")

    return resp


router = APIRouter()


@cbv(router)
class SimpleHandler:
    def __init__(self, request: Request) -> None:
        self.log = base_logger.getChild("request")
        request.state.log = self.log

    @router.get("/hello")
    async def hello(self):
        self.log.info("hello")
        return "Hello"

    @router.get("/bad_route")
    def bad_route(self):
        self.log.warning("going to throw an error!!!")
        raise HTTPException(status_code=500)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
