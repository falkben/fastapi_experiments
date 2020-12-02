from typing import Optional

import uvicorn
from fastapi import Body, Depends, FastAPI, Form, Query
from pydantic import BaseModel, Field, PrivateAttr

app = FastAPI()


# https://stackoverflow.com/questions/60127234/fastapi-form-data-with-pydantic-model
class CommonQueryParams(BaseModel):
    """
    Common Query Params for oauth functions
    **client_id** - OAuth client ID
    **conf** - OAuth client config
    **redirect_url** - The URL to send the temp token to
    **requested_scopes** - The access scopes requested by the client
    **state** - Random value that must match on return to client

    """

    client_id: Optional[str] = Field(None, description="The ID of the OAuth client")
    state: Optional[str] = Field(None, description="Client state")
    scope: Optional[str] = Field(None, description="Requested scopes")
    redirect_url: Optional[str] = Field(None, description="URL to redirect to")
    redirect_uri: Optional[str] = Field(
        None, description="Deprecated: URL to redirect to (use redirect_url)"
    )
    _something_else: str = PrivateAttr()

    # We can use an init here if we want to do something else to the args
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._something_else = "kookoo"

    @classmethod
    def as_form(
        cls,
        client_id: Optional[str] = Form(None),
        state: Optional[str] = Form(None),
        scope: Optional[str] = Form(None),
        redirect_url: Optional[str] = Form(None),
        redirect_uri: Optional[str] = Form(None),
    ):
        return cls(
            client_id=client_id,
            state=state,
            scope=scope,
            redirect_url=redirect_url,
            redirect_uri=redirect_uri,
        )

    @classmethod
    def as_json(
        cls,
        client_id: Optional[str] = Body(None),
        state: Optional[str] = Body(None),
        scope: Optional[str] = Body(None),
        redirect_url: Optional[str] = Body(None),
        redirect_uri: Optional[str] = Body(None),
    ):
        return cls(
            client_id=client_id,
            state=state,
            scope=scope,
            redirect_url=redirect_url,
            redirect_uri=redirect_uri,
        )

    @classmethod
    def as_query(
        cls,
        client_id: Optional[str] = Query(None),
        state: Optional[str] = Query(None),
        scope: Optional[str] = Query(None),
        redirect_url: Optional[str] = Query(None),
        redirect_uri: Optional[str] = Query(None),
    ):
        return cls(
            client_id=client_id,
            state=state,
            scope=scope,
            redirect_url=redirect_url,
            redirect_uri=redirect_uri,
        )


def combine_data(d1, d2):
    d1_defined = {k: v for k, v in d1.items() if v is not None}
    d2_defined = {k: v for k, v in d2.items() if v is not None}
    combined_data = dict(d1_defined, **d2_defined)
    return combined_data


@app.post("/query-form")
def post(
    form_data: CommonQueryParams = Depends(CommonQueryParams.as_form),
    query_data: CommonQueryParams = Depends(CommonQueryParams.as_query),
):
    # Order of combination would depend on what we want to take precedence
    combined_data = combine_data(form_data.dict(), query_data.dict())
    data = CommonQueryParams(**combined_data)
    print(form_data)
    print(query_data)
    return data


@app.post("/query-json")
def post2(
    json_data: CommonQueryParams = Depends(CommonQueryParams.as_json),
    query_data: CommonQueryParams = Depends(CommonQueryParams.as_query),
):
    combined_data = combine_data(json_data.dict(), query_data.dict())
    data = CommonQueryParams(**combined_data)
    print(json_data)
    print(query_data)
    return data


# This is not possible
# @app.post("/json-form")
# def post2(
#           form_data: CommonQueryParams = Depends(CommonQueryParams.as_form),
#           json_data: CommonQueryParams = Depends(CommonQueryParams.as_json)):
#     print(json_data)
#     print(form_data)


HOST = "localhost"
PORT = 8088

if __name__ == "__main__":
    uvicorn.run(app, port=PORT)
