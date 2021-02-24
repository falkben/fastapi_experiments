from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/hello")
def goodbye(request: Request):
    request.app.url_path_for("goodbye")
    return "hello"
