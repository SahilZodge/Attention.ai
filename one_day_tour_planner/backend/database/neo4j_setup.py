from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        """
        Initializes a connection to the Neo4j database.
        
        Args:
            uri (str): The URI of the Neo4j database.
            user (str): The username for the Neo4j database.
            password (str): The password for the Neo4j database.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("Connected to Neo4j Database")

    def close(self):
        """Closes the connection to the Neo4j database."""
        if self.driver:
            self.driver.close()
            print("Disconnected from Neo4j Database")

    def create_indexes(self):
        """
        Creates indexes on commonly queried nodes to optimize performance.
        This method sets up indexes on `User` nodes by `id`, `Preference` nodes by `key` and `value`,
        and `Trip` nodes by `id`.
        """
        index_queries = [
            "CREATE INDEX IF NOT EXISTS FOR (u:User) ON (u.id)",
            "CREATE INDEX IF NOT EXISTS FOR (p:Preference) ON (p.key, p.value)",
            "CREATE INDEX IF NOT EXISTS FOR (t:Trip) ON (t.id)"
        ]
        with self.driver.session() as session:
            for query in index_queries:
                session.run(query)
        print("Indexes created successfully")

    def reset_database(self):
        """
        Resets the database by deleting all nodes and relationships.
        This method is useful for testing and development but should be used with caution
        in production environments.
        """
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("Database reset: all nodes and relationships deleted")

    def setup_database(self):
        """
        Sets up the initial database schema by creating necessary indexes and constraints.
        Call this method to prepare the database for use.
        """
        self.create_indexes()
        print("Database setup complete")
