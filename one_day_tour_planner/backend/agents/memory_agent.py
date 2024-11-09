from neo4j import GraphDatabase
from typing import Optional, Dict

class MemoryAgent:
    def __init__(self, uri: str, user: str, password: str):
        # Initialize Neo4j driver with provided credentials
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def store_preference(self, user_id: str, key: str, value: str):
        """
        Stores a single user preference as a relationship in the Neo4j graph.

        Args:
            user_id (str): The unique identifier for the user.
            key (str): The preference key (e.g., "city", "budget").
            value (str): The value of the preference (e.g., "Rome", "50").
        """
        query = """
        MERGE (u:User {id: $user_id})
        MERGE (p:Preference {key: $key, value: $value})
        MERGE (u)-[:HAS_PREFERENCE]->(p)
        """
        with self.driver.session() as session:
            session.run(query, user_id=user_id, key=key, value=value)

    def fetch_preferences(self, user_id: str) -> Optional[Dict[str, str]]:
        """
        Retrieves all stored preferences for a specific user.

        Args:
            user_id (str): The unique identifier for the user.

        Returns:
            dict: A dictionary of preferences, where keys are preference types and values are preference values.
        """
        query = """
        MATCH (u:User {id: $user_id})-[:HAS_PREFERENCE]->(p:Preference)
        RETURN p.key AS key, p.value AS value
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            preferences = {record["key"]: record["value"] for record in result}
        return preferences if preferences else None

    def update_preference(self, user_id: str, key: str, new_value: str):
        """
        Updates an existing user preference in the Neo4j graph.

        Args:
            user_id (str): The unique identifier for the user.
            key (str): The preference key to update.
            new_value (str): The new value for the preference.
        """
        query = """
        MATCH (u:User {id: $user_id})-[:HAS_PREFERENCE]->(p:Preference {key: $key})
        SET p.value = $new_value
        """
        with self.driver.session() as session:
            session.run(query, user_id=user_id, key=key, new_value=new_value)

    def store_trip_history(self, user_id: str, trip_id: str, trip_data: Dict[str, str]):
        """
        Stores a trip history record in the Neo4j graph, associating it with the user.

        Args:
            user_id (str): The unique identifier for the user.
            trip_id (str): Unique identifier for the trip.
            trip_data (dict): A dictionary of trip details (e.g., {"destination": "Rome", "date": "2023-11-10"}).
        """
        query = """
        MERGE (u:User {id: $user_id})
        MERGE (t:Trip {id: $trip_id})
        SET t += $trip_data
        MERGE (u)-[:HAS_TRIP]->(t)
        """
        with self.driver.session() as session:
            session.run(query, user_id=user_id, trip_id=trip_id, trip_data=trip_data)

    def fetch_trip_history(self, user_id: str) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Retrieves all trip history records for a specific user.

        Args:
            user_id (str): The unique identifier for the user.

        Returns:
            dict: A dictionary of trips, where keys are trip IDs and values are dictionaries of trip details.
        """
        query = """
        MATCH (u:User {id: $user_id})-[:HAS_TRIP]->(t:Trip)
        RETURN t.id AS trip_id, t
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            trips = {record["trip_id"]: dict(record["t"]) for record in result}
        return trips if trips else None

    def close(self):
        """
        Closes the Neo4j driver session.
        """
        self.driver.close()
