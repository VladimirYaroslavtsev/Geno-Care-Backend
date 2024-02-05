from types import AsyncGeneratorType
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
import openai as ai
import uvicorn
import db
import utils as ut


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# crud = db.Neo4jCRUD()
# crud.connect()

with open('chat_index.html', 'r') as f:
    html = f.read()


@app.get('/')
async def web_app() -> HTMLResponse:
    return HTMLResponse(html)


@app.get('/healthcheck')
def healthcheck():
    return {
        'status': 'ok'
    }


@app.websocket('/ws')
async def ws_endp(websocket: WebSocket) -> None:
    await websocket.accept()

    while True:
        await websocket.send_text('Healthcare Assistant')
        
        message = await websocket.receive_text()
        async for text in ut.generate_description(message):
            await websocket.send_text(text)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='debug', reload=True)
