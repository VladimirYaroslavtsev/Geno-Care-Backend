import json
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import db
import dependency
import settings as st
import utils as ut


router = APIRouter(tags=['recommendations'])


@router.get('/v1/recommendations')
async def get_recommendations(
    node_id_cookie: int = Depends(dependency.get_node_id_cookie),
    tree_db: db.Neo4jCRUD = Depends(dependency.get_database_connection)
) -> JSONResponse:
    raw_recommedations = ''
    try:
        status_code = 200
        message = generate_user_recommendation_message(node_id_cookie, tree_db)
        messages = ut.get_messages(message, st.RECOMMENDATION_SYSTEM_MESSAGE)

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


def generate_user_recommendation_message(node_id: int, tree_db: db.Neo4jCRUD):
    family_tree = tree_db.get_family_tree(node_id)
    message = 'Give me health recommendations.'

    if len(family_tree) == 1:
        message += f' This my general information: {family_tree}. No relative info to provide.'
    else:
        message += f'Here is mine and my family information: {family_tree}.'
    
    return message
