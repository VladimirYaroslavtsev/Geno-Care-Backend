from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import db
import dependency
import models
import settings as st
import utils as ut
import json


router = APIRouter(tags=['family_tree'])


@router.get('/v1/family_tree')
async def get_family_tree_route(
    node_id_cookie: int = Depends(dependency.get_node_id_cookie),
    tree_db: db.Neo4jCRUD = Depends(dependency.get_database_connection)
) -> JSONResponse:
    family_tree = tree_db.get_family_tree(node_id_cookie)
    print(family_tree)
    return JSONResponse(content=family_tree)


@router.get('/v1/profile', response_model=models.Profile)
async def get_family_tree_route(
    node_id_cookie: int = Depends(dependency.get_node_id_cookie),
    tree_db: db.Neo4jCRUD = Depends(dependency.get_database_connection)
):
    profile = tree_db.read_node(node_id_cookie)
    print(profile)
    return JSONResponse(content=profile)
