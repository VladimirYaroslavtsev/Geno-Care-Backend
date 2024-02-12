from fastapi import HTTPException, Request
import db
import settings as st


def get_database_connection():
    print(st.NEO4J_IP)
    # bolt://172.17.0.2:7687
    uri = f'bolt://{st.NEO4J_IP}:7687'
    tree_db = db.Neo4jCRUD(uri, st.USER, st.PASSWORD)
    tree_db.connect()
    tree_db.test_query()
    return tree_db


async def get_node_id_cookie(request: Request):
    node_id_cookie = request.cookies.get('node_id')
    if node_id_cookie is None:
        raise HTTPException(status_code=401, detail='Cookie not found')
    return node_id_cookie
