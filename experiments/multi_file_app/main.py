from fastapi import FastAPI

from experiments.multi_file_app.routerA import router as routerA
from experiments.multi_file_app.routerB import router as routerB

app = FastAPI()

app.include_router(routerB)
app.include_router(routerA)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
