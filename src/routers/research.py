from fastapi import APIRouter, Request, Depends, WebSocket
from fastapi.responses import JSONResponse

import settings as st
import utils as ut


router = APIRouter(tags=['research'])


@router.websocket('/wc_research')
async def ws_endp(websocket: WebSocket) -> None:
    await websocket.accept()

    while True:
        await websocket.send_text(st.START_MESSAGE)
        message = await websocket.receive_text()
        
        async for text in ut.generate_description(message, st.RESEARCH_SYSTEM_MESSAGE):
            await websocket.send_text(text)
