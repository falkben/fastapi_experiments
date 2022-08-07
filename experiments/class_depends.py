from typing import List

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi_utils.cbv import cbv

router = APIRouter()


def depends_method(names: List[str] = Query(..., description="list of names")):
    return names


@cbv(router)
class BaseClass:
    str_attr: str = "hello"

    def __init__(self):
        self.int_attr = 10

    def depends_class_method(
        self, names: List[str] = Query(..., description="list of names")
    ):
        names_str = ", ".join(names)
        return f"{self.str_attr} {names_str}"

    def class_method(self, names):
        names_str = ", ".join(names)
        return f"{self.str_attr} {names_str}"

    @router.get("/class_attr")
    def class_attr(self):
        return self.str_attr

    @router.get("/init_attr")
    def init_attr(self):
        return self.int_attr

    @router.get("/class_method_depends")
    def class_method_depends(self, names=Depends(depends_class_method)):
        """this doesn't work because the dependency cannot be a class method"""
        return names

    @router.get("/class_method_and_depends")
    def class_method_and_depends(self, names=Depends(depends_method)):
        return self.class_method(names)


app = FastAPI()
app.include_router(router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
