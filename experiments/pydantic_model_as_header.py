from fastapi import Depends, FastAPI, Header, Request
from pydantic import BaseModel


def as_header(cls):
    """decorator for pydantic model
    replaces the Signature of the parameters of the pydantic model with `Header`
    """
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(
                default=Header(...) if arg.default is arg.empty else Header(arg.default)
            )
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@as_header
class ApiVersionInfo(BaseModel):
    api_version: int
    resource_version: int


def set_api_version_info(
    request: Request, api_ver: ApiVersionInfo = Depends(ApiVersionInfo)
):
    request.state.api_info = api_ver.api_version


app = FastAPI(dependencies=[Depends(set_api_version_info)])


@app.get("/")
def get_api_version_info(request: Request):
    return request.state.api_info


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
