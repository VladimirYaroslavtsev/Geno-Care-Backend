import json
from fastapi import APIRouter, Request, Depends, WebSocket
from fastapi.responses import JSONResponse
import settings as st
import utils as ut


router = APIRouter(tags=['recommendations'])


@router.get('/v1/recommendations')
async def get_recommendations() -> JSONResponse:
    raw_recommedations = ''
    try:
        status_code = 200
        family_info = 'Provide me health recommendations. I don\'t have relatives information to provide.'
        messages = ut.get_messages(family_info, st.RECOMMENDATION_SYSTEM_MESSAGE)

        async for text in ut.generate_description(messages):
            raw_recommedations += text
        content = raw_recommedations.replace('\n', '').replace('\r', '').replace('\t', '')

        try:
            content=json.loads(content)
        except Exception as err:
            print(err)
            content = raw_recommedations
    except Exception as err:
        print(err)
        status_code = 500
    return JSONResponse(
        content=content,
        status_code=status_code
    )
