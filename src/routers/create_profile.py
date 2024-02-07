from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
import db
import dependency
import models
import settings as st
import utils as ut
import json

router = APIRouter(tags=['create_profile'])


@router.post('/create_profile')
async def create_profile(profile: models.Profile, tree_db: db.Neo4jCRUD = Depends(dependency.get_database_connection)):
    status_code = 201
    result = 'The profile successfuly created'
    try:
        data = json.loads(profile.model_dump_json())
        print(data)
        
        res = tree_db.create_node(profile.name, **data)
        print(res)

    except Exception as err:
        print(err)
        status_code = 500
        result = 'Couldn\'t create profile'

    return JSONResponse(
        status_code=status_code,
        content=result,
        headers=st.HEADERS
    )
