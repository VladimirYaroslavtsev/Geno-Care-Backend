from neo4j import GraphDatabase


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
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def create_node(self, label, **properties):
        with self._driver.session() as session:
            result = session.write_transaction(self._create_node, label, properties)
            return result

    def _create_node(self, tx, label, properties):
        query = (
            f"CREATE (node:{label} $properties) "
            "RETURN id(node) AS node_id, node"
        )
        return tx.run(query, properties=properties).single()

    def read_node(self, node_id):
        with self._driver.session() as session:
            result = session.read_transaction(self._read_node, node_id)
            return result

    def _read_node(self, tx, node_id):
        query = "MATCH (node) WHERE id(node) = $node_id RETURN node"
        return tx.run(query, node_id=node_id).single()

    def update_node(self, node_id, **properties):
        with self._driver.session() as session:
            result = session.write_transaction(self._update_node, node_id, properties)
            return result

    def _update_node(self, tx, node_id, properties):
        query = (
            "MATCH (node) "
            "WHERE id(node) = $node_id "
            "SET node += $properties "
            "RETURN id(node) AS node_id, node"
        )
        return tx.run(query, node_id=node_id, properties=properties).single()

    def delete_node(self, node_id):
        with self._driver.session() as session:
            session.write_transaction(self._delete_node, node_id)

    def _delete_node(self, tx, node_id):
        query = "MATCH (node) WHERE id(node) = $node_id DELETE node"
        tx.run(query, node_id=node_id)
