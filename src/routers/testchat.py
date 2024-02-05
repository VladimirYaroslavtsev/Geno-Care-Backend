import openai


from types import AsyncGeneratorType
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import openai as ai
import uvicorn
import db
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
    allow_headers=["*"],
    allow_origins=["*"],
    allow_methods=["*"],
)
app.include_router(create_profile.router)
app.include_router(family_tree.router)
app.include_router(recomendation.router)
app.include_router(research.router)


# crud = db.Neo4jCRUD(st.URI, st.USER, st.PASSWORD)
# crud.connect()

# with open('static/chat_index.html', 'r') as f:
#     html = f.read()


@app.get('/')
async def web_app() -> HTMLResponse:
    # return HTMLResponse(html)
    return FileResponse('src/static/chat_index.html', media_type='text/html')


@app.get('/healthcheck')
def healthcheck():
    return {
        'status': 'ok',
        'version': st.VERSION
    }


# @app.websocket('/ws')
# async def ws_endp(websocket: WebSocket) -> None:
#     await websocket.accept()

#     while True:
#         await websocket.send_text(st.START_MESSAGE)
#         message = await websocket.receive_text()

#         async for text in ut.generate_description(message):
#             await websocket.send_text(text)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='debug', reload=True)
