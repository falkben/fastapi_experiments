""" fastapi_utils double adds prefixes """

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

# fastapi_restful does not double add prefixes
# from fastapi_restful.cbv import cbv

router = APIRouter(prefix="/api/v1")


@cbv(router)
class C:
    @router.get("/")
    def f(self):
        ...


def test_router_prefix():
    assert router.routes[-1].path == "/api/v1/api/v1/"
