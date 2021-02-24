from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/goodbye")
def goodbye(request: Request):
    request.app.url_path_for("hello")
    return "goodbye"
