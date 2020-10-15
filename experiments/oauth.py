""" Oauth client using authlib """

import json
import os

import httpx
import uvicorn
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

OAUTH2_CLIENT_ID = os.environ.get("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.environ.get("OAUTH2_CLIENT_SECRET")
OAUTH2_TOKEN_URL = os.environ.get("OAUTH2_TOKEN_URL")
OAUTH2_AUTHORIZE_URL = os.environ.get("OAUTH2_AUTHORIZE_URL")
OAUTH2_SCOPE = os.environ.get("OAUTH2_SCOPE")
OAUTH2_USER_INFO_URL = os.environ.get("OAUTH2_USER_INFO_URL")

HOST = "localhost"
PORT = 8000

oauth = OAuth()
oauth.register(
    name="mast",
    client_id=OAUTH2_CLIENT_ID,
    client_secret=OAUTH2_CLIENT_SECRET,
    access_token_url=OAUTH2_TOKEN_URL,
    # access_token_params=None,
    authorize_url=OAUTH2_AUTHORIZE_URL,
    # authorize_params=None,
    # api_base_url='https://api.github.com/',
    client_kwargs={
        "scope": OAUTH2_SCOPE,
        "token_endpoint_auth_method": "client_secret_basic",
    },
)

app = FastAPI()
# we need this to save temporary code & state in session
app.add_middleware(SessionMiddleware, secret_key="some-random-string")


@app.get("/login")
async def login(request: Request):
    redirect_uri = f"http://{HOST}:{PORT}/callback"
    return await oauth.mast.authorize_redirect(request, redirect_uri)


async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"token {access_token}",
            "accept": "application/json",
        }
        resp = await client.get(OAUTH2_USER_INFO_URL, headers=headers)
        return resp.json()


@app.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.mast.authorize_access_token(request)
    user = await get_user_info(token["access_token"])
    request.session["user"] = dict(user)
    return RedirectResponse(url="/")


@app.route("/")
async def homepage(request: Request):
    user = request.session.get("user")
    if user:
        data = json.dumps(user)
        html = f"<pre>{data}</pre>" '<a href="/logout">logout</a>'
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@app.route("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
