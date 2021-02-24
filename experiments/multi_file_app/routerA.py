from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/hello")
def hello(request: Request):
    request.app.url_path_for("goodbye")
    return "hello"
