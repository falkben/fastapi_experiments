import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/hello")
def return_file():
    def file_gen(file_path):
        with open(file_path) as f:
            for line in f:
                yield line

    return StreamingResponse(file_gen(f"{__file__}"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
