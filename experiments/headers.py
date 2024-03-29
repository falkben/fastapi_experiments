import json

import uvicorn
from fastapi import FastAPI, Header, Path
from fastapi.responses import HTMLResponse, Response, StreamingResponse, FileResponse

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


@app.get("/accept")
async def accept(name: str = "bob", accept=Header("")):
    """by default we always return json"""

    return {"hello": name, "accept": accept}


@app.get("/accept_custom")
async def accept_custom_resp(name: str = "bob", accept=Header(None)):
    """Content-Type header is set by using the media_type argument to Response"""

    if accept is None or accept == "*/*":  # test client uses */* for accept header
        accept = "application/json"
    data = {"hello": name, "accept": accept}
    return Response(content=json.dumps(data), media_type=accept)


@app.get("/accept-path/{filename:path}")
async def accept_path(name: str = "bob", filename=Path(None), accept=Header(None)):

    content_types = {"xml": "text/xml", "json": "application/json", "csv": "text/csv"}
    extension = filename.split(".")[-1]
    content_types.get(extension, "application/json")
    if "xml" in accept or "xml" in extension:
        # this matches default browser requests because they have "xml" in them
        media_type = content_types.get("xml")
    else:
        media_type = content_types.get(extension, "application/json")

    data = {"hello": name, "accept": accept}
    return Response(content=json.dumps(data), media_type=media_type)


@app.get("/accept_stream")
async def accept_stream(name: str = "bob", accept=Header(None)):
    """Content-Type header is set by using the media_type argument to Streaming Response"""

    if accept is None or accept == "*/*":  # test client uses */* for accept header
        accept = "application/json"

    # we need a gen here:
    data = {"hello": name, "accept": accept}

    def gen():
        """generator that returns a dictionary"""
        yield "{"
        for i, (k, v) in enumerate(data.items()):
            yield f'"{k}":"{v}"'
            if i != len(data) - 1:
                yield ","
        yield "}"

    return StreamingResponse(gen(), media_type=accept)


@app.get("/file_stream")
async def return_file():
    return FileResponse(f"{__file__}", filename=f"{__file__}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
