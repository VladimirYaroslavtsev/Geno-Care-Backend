import json
import re
from fastapi import APIRouter, Request, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import db
import dependency
import settings as st
import utils as ut


router = APIRouter(tags=['research'])


@router.websocket('/v1/wc_research')
async def ws_endp(
    websocket: WebSocket,
    # request: Request,
    # node_id_cookie: int = Depends(dependency.get_node_id_cookie),
    tree_db: db.Neo4jCRUD = Depends(dependency.get_database_connection)
) -> None:
    # print(request)
    try:
        await websocket.accept()
        messages = []
        family_json = None
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

            async for text in ut.generate_description(messages):
                if 'summary' in text or len(text.split('#')) == 2:
                    print(text)
                    summary = text.split('#')
                    text = summary[0]
                    json_summary = summary[-1].replace('\n', '').replace('\r', '').replace('\t', '')
                    print(json_summary)
                    family_json = json.loads(json_summary)
                    print(family_json)

                messages.append({'role': 'assistant', 'content': text})
                await websocket.send_text(text)
    except WebSocketDisconnect as err:
        print(err)
        print('disconnecting...')
    finally:
        if family_json:
            print('Adding/updating family members')
            for family_member in family_json['family']:
                # pass
                tree_db.create_family_member(node_id=0, family_member_data=family_member)
