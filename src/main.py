from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import jwt
import requests
import uvicorn
from routers import (
    create_profile, family_tree, recomendation, research
)
import settings as st
import utils as ut


app = FastAPI(debug=True, version=st.VERSION)
app.mount('/src/static', StaticFiles(directory='src/static'), name='static')
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=['*'],
    allow_origins=['*'],
    allow_methods=['*'],
)
app.include_router(create_profile.router)
app.include_router(family_tree.router)
app.include_router(recomendation.router)
app.include_router(research.router)


@app.get('/')
async def web_app() -> HTMLResponse:
    return FileResponse('src/static/chat_index.html', media_type='text/html')


@app.get('/healthcheck')
def healthcheck():
    return {
        'status': 'ok',
        'version': st.VERSION
    }


@app.get('/login/callback')
async def login_callback(code: Optional[str] = None, error: Optional[str] = None):
    if error:
        raise HTTPException(status_code=400, detail=error)
    if not code:
        raise HTTPException(status_code=400, detail='Code parameter is missing')

    data = {
        'code': code,
        'client_id': st.GOOGLE_CLIENT_ID,
        'client_secret': st.GOOGLE_CLIENT_SECRET,
        'redirect_uri': st.REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post('https://oauth2.googleapis.com/token', data=data)
    response_data = response.json()

    if 'access_token' not in response_data:
        raise HTTPException(status_code=400, detail='Failed to retrieve access token')

    access_token = response_data['access_token']

    # Validate access token
    userinfo_response = requests.get(
        f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}'
    )
    userinfo_data = userinfo_response.json()

    if 'error' in userinfo_data:
        raise HTTPException(status_code=400, detail='Failed to retrieve user info')

    token_data = {'sub': userinfo_data['sub']}
    token = jwt.encode(token_data, st.JWT_SECRET, algorithm=st.JWT_ALGORITHM)

    redirect_url = f'http://localhost:3000?token={token}'
    return RedirectResponse(url=redirect_url)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='debug', reload=True)
