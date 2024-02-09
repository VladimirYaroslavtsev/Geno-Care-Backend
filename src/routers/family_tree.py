from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
import db
import dependency
import models
import settings as st
import utils as ut
import json


router = APIRouter(tags=['family_tree'])


@router.get("/family/{person_name}/tree", response_model=models.FamilyTree)
async def get_family_tree_route(person_name: str, tree_db: db.Neo4jCRUD = Depends(dependency.get_database_connection)):
    family_tree = tree_db.get_family_tree(person_name, tree_db)
    return JSONResponse(content=family_tree.dict())
