from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import JSONResponse
import models
import settings as st


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f'https://accounts.google.com/o/oauth2/v2/auth?\
        client_id={st.GOOGLE_CLIENT_ID}&redirect_uri={st.REDIRECT_URI}&response_type=code&scope=openid%20email%20profile',
)
