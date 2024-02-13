from typing import Any, Dict, List
from fastapi.exceptions import HTTPException
from neo4j import GraphDatabase
import models


class Neo4jCRUD:

    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        print(self._uri)
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def test_query(self):
        try:
            query = 'Match () Return 1 Limit 1'
            with self._driver.session() as session:
                session.run(query)
                print('Works')
        except Exception as err:
            print(err)
            print('Doesnt work')

    def create_node(self, label: str, **properties):
        print(properties)
        with self._driver.session() as session:
            result = session.write_transaction(self._create_node, label, properties)
            return result

    def _create_node(self, tx, label, properties):
        query = (
            f'CREATE (node:{label} $properties) '
            'RETURN id(node) AS node_id, node'
        )
        return tx.run(query, properties=properties).single()

    def read_node(self, node_id):
        print(node_id)
        with self._driver.session() as session:
            result = session.read_transaction(self._read_node, node_id)
            return result

    def _read_node(self, tx, node_id: int):
        query = 'MATCH (node) WHERE id(node) = $node_id RETURN node'
        result = tx.run(query, node_id=int(node_id)).single()
        print(result)
        if result:
            node_properties = dict(result['node'])
            return node_properties
        else:
            return None

    def create_family_member(self, node_id: int, family_member_data: Dict[str, Any]):
        with self._driver.session() as session:
            query = '''
            MATCH (node)
            WHERE id(node) = $user_node_id
            CREATE (node)-[:FAMILY_MEMBER {family_status: $family_status}]->(family_member:FamilyMember $family_member_properties)
            RETURN family_member
            '''
            family_member_properties = {
                'name': family_member_data['name'],
                'age': family_member_data['age'],
                'family_status': family_member_data['family_status'],
                'medical_conditions': family_member_data.get('medical_conditions', [])
            }
            result = session.run(
                query,
                user_node_id=int(node_id),
                family_status=family_member_properties['family_status'],
                family_member_properties=family_member_properties
            )
            return result.single()['family_member']

    def get_family_tree(self, node_id: int) -> List[Dict[str, Any]]:
        with self._driver.session() as session:
            query = '''
            MATCH (n)-[]-(connected_node)
            WHERE id(n) = $node_id
            RETURN n AS node
            UNION
            MATCH (n)-[]-(connected_node)
            WHERE id(n) = $node_id
            RETURN connected_node AS node
            '''
            result = session.run(query, node_id=int(node_id))
            connected_nodes = [dict(record['node']) for record in result]
            return connected_nodes

    def update_node(self, node_id, **properties):
        with self._driver.session() as session:
            result = session.write_transaction(self._update_node, node_id, properties)
            return result

    def _update_node(self, tx, node_id, properties):
        query = (
            'MATCH (node) '
            'WHERE id(node) = $node_id '
            'SET node += $properties '
            'RETURN id(node) AS node_id, node'
        )
        return tx.run(query, node_id=node_id, properties=properties).single()

    def delete_node(self, node_id):
        with self._driver.session() as session:
            session.write_transaction(self._delete_node, node_id)

    def _delete_node(self, tx, node_id):
        query = 'MATCH (node) WHERE id(node) = $node_id DELETE node'
        tx.run(query, node_id=node_id)
