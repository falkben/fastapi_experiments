# requirements:
# elastic-apm
# psutil

import asyncio
import os
import time

from dotenv import load_dotenv
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import Depends, FastAPI

load_dotenv()

ELASTIC_SERVICE_NAME = os.getenv("ELASTIC_SERVICE_NAME")
ELASTIC_APM_SERVER_URL = os.getenv("ELASTIC_APM_SERVER_URL")

apm = make_apm_client(
    {"SERVICE_NAME": ELASTIC_SERVICE_NAME, "SERVER_URL": ELASTIC_APM_SERVER_URL}
)
app = FastAPI()
app.add_middleware(ElasticAPM, client=apm)


def waiting_dep():
    time.sleep(0.1)


@app.get("/hello", dependencies=[Depends(waiting_dep)])
async def hello():
    await asyncio.sleep(0.1)
    return "hello"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
