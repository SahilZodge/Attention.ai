from pydantic import BaseModel
from typing import List, Optional
from agents.memory_agent import MemoryAgent

# Define the User Preferences data model
class UserPreferences(BaseModel):
    city: str
    start_time: str
    end_time: str
    budget: float
    interests: List[str]
    starting_point: Optional[str] = None

# User Interaction Agent to handle collecting and storing user preferences
class UserInteractionAgent:
    def __init__(self):
        # Initialize memory agent for storing and retrieving preferences
        self.memory_agent = MemoryAgent()

    def collect_preferences(self, preferences: UserPreferences):
        """
        Collects and stores user preferences in memory for personalization.
        """
        # Convert preferences to a dictionary for easier handling
        preferences_data = preferences.dict()
        
        # Store each preference as a relationship in memory using the MemoryAgent
        user_id = self.generate_user_id(preferences)  # Generate or retrieve a user ID
        for key, value in preferences_data.items():
            self.memory_agent.store_preference(user_id, key, value)
        
        # Return confirmation of stored preferences
        return {"status": "success", "message": "User preferences collected and stored successfully"}

    def retrieve_preferences(self, user_id: str) -> dict:
        """
        Retrieves user preferences from memory for a given user_id.
        """
        # Query the MemoryAgent to get stored preferences
        preferences = self.memory_agent.fetch_preferences(user_id)
        if preferences:
            return preferences
        else:
            return {"status": "error", "message": "No preferences found for this user"}

    def update_preference(self, user_id: str, key: str, value: str):
        """
        Updates a specific user preference in memory.
        """
        # Update the preference using the MemoryAgent
        self.memory_agent.store_preference(user_id, key, value)
        return {"status": "success", "message": f"Preference '{key}' updated successfully"}

    def generate_user_id(self, preferences: UserPreferences) -> str:
        """
        Generates a unique user ID based on user preferences.
        Here, we'll simply use the city and start_time for simplicity,
        but a more robust system could use unique identifiers.
        """
        return f"{preferences.city}_{preferences.start_time}"
