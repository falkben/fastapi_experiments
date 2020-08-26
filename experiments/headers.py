import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/hello")
async def hello():
    """
    header "fields" (keys) are case insensitive
    https://tools.ietf.org/html/rfc2616#section-4.2
    fastapi always lower cases them
    """

    headers = {"CONTENT-SECURITY-POLICY": "default-src 'self'"}
    return HTMLResponse(content="hello", headers=headers)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
