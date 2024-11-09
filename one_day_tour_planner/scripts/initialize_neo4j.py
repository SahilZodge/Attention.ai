from neo4j import GraphDatabase

def initialize_db(uri: str, user: str, password: str):
    """
    Initializes the Neo4j database by creating initial nodes and relationships.
    This function ensures that the database is set up with the required structure.
    
    Args:
        uri (str): The URI of the Neo4j database.
        user (str): The username to connect to Neo4j.
        password (str): The password to connect to Neo4j.
    """
    # Connect to the Neo4j database
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    # Create initial nodes and relationships
    with driver.session() as session:
        try:
            # Create sample nodes for User, Preferences, and Trip
            session.run("""
            MERGE (u:User {id: '1', name: 'John Doe'})
            MERGE (p:Preference {key: 'city', value: 'Paris'})
            MERGE (t:Trip {id: '1', destination: 'Paris', date: '2024-12-01'})
            MERGE (u)-[:HAS_PREFERENCE]->(p)
            MERGE (u)-[:HAS_TRIP]->(t)
            """)
            print("Database initialized successfully with sample nodes.")
        
        except Exception as e:
            print(f"Error initializing the database: {e}")
    
    # Close the connection
    driver.close()
