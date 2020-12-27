import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/fail")
def failing_endpoint():
    raise HTTPException(500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
