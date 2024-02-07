from fastapi import APIRouter, Request, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

import settings as st
import utils as ut


router = APIRouter(tags=['research'])


@router.websocket('/v1/wc_research')
async def ws_endp(websocket: WebSocket) -> None:
    try:
        await websocket.accept()
        messages = []

        while True:
            # await websocket.send_text(st.START_MESSAGE)
            message = await websocket.receive_text()

            # Need to create a better context manager for it.
            if messages:
                messages.append(
                    {
                        'role': 'user',
                        'content': f'{st.DELIMITER}{message}{st.DELIMITER}'
                    }
                )
            else:
                messages = ut.get_messages(message, st.RESEARCH_SYSTEM_MESSAGE)

            print('*****************')
            print(messages)
            print('*****************')
            async for text in ut.generate_description(messages):
                messages.append({'role': 'assistant', 'content': text})
                await websocket.send_text(text)
    except WebSocketDisconnect as err:
        print(err)
        print('disconnecting...')
