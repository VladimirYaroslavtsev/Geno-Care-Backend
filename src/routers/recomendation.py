from fastapi import APIRouter, Request, Depends, WebSocket
from fastapi.responses import JSONResponse
import settings as st
import utils as ut


router = APIRouter(tags=['recommendations'])


@router.websocket('/v1/wc_recommendations')
async def ws_endp(websocket: WebSocket) -> None:
    await websocket.accept()

    while True:
        # await websocket.send_text(st.START_MESSAGE)
        message = await websocket.receive_text()
        messages = ut.get_messages(message, st.RECOMMENDATION_SYSTEM_MESSAGE)
        print('*****************')
        print(messages)
        print('*****************')
        async for text in ut.generate_description(messages):
            await websocket.send_text(text)
