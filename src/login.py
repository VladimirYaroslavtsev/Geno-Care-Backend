from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import JSONResponse
from social_core.utils import parse_qs

from routes import (
    create_profile, family_tree, recomendation, research
)


app = FastAPI()

SECRET = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Setup fastapi-login
manager = LoginManager(SECRET, tokenUrl="/token", use_cookie=True, use_header=False)

# Setup OAuth2
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token", authorizationUrl="login", auto_error=False
)


@app.get("/login")
async def login(request: Request, login_manager: LoginManager = Depends()):
    return await login_manager.google_login(request)


@app.get("/login/callback")
async def login_callback(request: Request, login_manager: LoginManager = Depends()):
    response = await login_manager.google_callback(request)
    return response


@app.get("/logout")
async def logout(request: Request, login_manager: LoginManager = Depends()):
    return await login_manager.logout(request, redirect_uri="/")


@app.get("/token")
async def token(request: Request, credentials: OAuth2AuthorizationCodeBearer = Depends(oauth2_scheme)):
    return await login_manager.google_oauth2_authorize(request, credentials)


# Example protected route
@app.get("/protected")
async def protected_route(request: Request, current_user: User = Depends(manager)):
    return {"message": "This is a protected route", "user": current_user}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
