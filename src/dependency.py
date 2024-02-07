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
