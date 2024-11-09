import sys
sys.path.append("D:\IIT BOMBAY\Placement Prep\Assignments\Attentions.ai\one_day_tour_planner")
import requests
import json
from huggingface_integration import HuggingFaceIntegration  # Replaced OpenAI integration with Hugging Face
from backend.database.schemas.user_preferences import UserPreferences
from neo4j import GraphDatabase
from typing import Dict, Optional

class APIRequests:
    """
    This class handles all the API requests for processing user preferences, interacting with the database,
    and generating responses based on the preferences provided.
    """

    def __init__(self, neo4j_driver: GraphDatabase, huggingface_integration: HuggingFaceIntegration):
        """
        Initializes the APIRequests instance with the required database driver and HuggingFace integration instance.

        Args:
            neo4j_driver (GraphDatabase): A connected Neo4j driver instance to interact with the database.
            huggingface_integration (HuggingFaceIntegration): An instance of HuggingFaceIntegration to generate responses.
        """
        self.neo4j_driver = neo4j_driver
        self.huggingface_integration = huggingface_integration

    def collect_preferences(self, preferences: Dict[str, str]) -> Optional[str]:
        """
        Collects user preferences and processes them to generate a one-day tour plan.

        Args:
            preferences (Dict[str, str]): The dictionary containing user preferences such as city, start time, and budget.

        Returns:
            Optional[str]: The generated response containing the personalized tour plan or suggestions.
        """
        # Step 1: Validate preferences (ensure required fields are provided)
        user_preferences = self.validate_preferences(preferences)
        if not user_preferences:
            return "Invalid input. Please provide complete preferences."

        # Step 2: Check the city and budget in the database (Neo4j)
        city_info = self.get_city_info_from_db(user_preferences.city)
        if not city_info:
            return f"Sorry, we don't have information about {user_preferences.city}. Please try a different city."

        # Step 3: Generate tour plan using AI (Hugging Face)
        generated_plan = self.generate_tour_plan(user_preferences)

        # Step 4: Return the generated tour plan
        return generated_plan

    def validate_preferences(self, preferences: Dict[str, str]) -> Optional[UserPreferences]:
        """
        Validates and converts raw input preferences into a structured UserPreferences object.

        Args:
            preferences (Dict[str, str]): The raw dictionary containing user input.

        Returns:
            UserPreferences: A Pydantic model instance if the data is valid, or None if invalid.
        """
        try:
            user_preferences = UserPreferences(**preferences)
            return user_preferences
        except Exception as e:
            print(f"Validation error: {e}")
            return None

    def get_city_info_from_db(self, city: str) -> Optional[Dict]:
        """
        Fetches city-related information from the Neo4j database to check for available tours, activities, etc.

        Args:
            city (str): The city name provided by the user.

        Returns:
            Optional[Dict]: The city-related data if found, or None if not found.
        """
        query = f"""
        MATCH (c:City {{name: '{city}'}})
        RETURN c.name AS city, c.description AS description, c.activities AS activities
        """
        with self.neo4j_driver.session() as session:
            result = session.run(query)
            city_info = result.single()
            if city_info:
                return {
                    "city": city_info["city"],
                    "description": city_info["description"],
                    "activities": city_info["activities"]
                }
            return None

    def generate_tour_plan(self, preferences: UserPreferences) -> str:
        """
        Generates a one-day tour plan based on user preferences using Hugging Face model.

        Args:
            preferences (UserPreferences): The validated user preferences.

        Returns:
            str: The generated tour plan.
        """
        # Construct a prompt based on preferences (could use city, start time, budget, etc.)
        prompt = f"Create a fun and engaging one-day tour plan for {preferences.city} starting at {preferences.start_time} with a budget of {preferences.budget}. Include activities that align with the user's interests like {', '.join(preferences.interests)}."

        # Use Hugging Face to generate a tour plan (using text generation model like GPT-2, T5, etc.)
        generated_text = self.huggingface_integration.generate_text(prompt)
        
        return generated_text

    def get_additional_suggestions(self, city: str) -> str:
        """
        Fetches additional activity suggestions for a given city using Hugging Face model.

        Args:
            city (str): The name of the city to fetch activity suggestions for.

        Returns:
            str: The AI-generated activity suggestions.
        """
        prompt = f"Suggest additional activities and hidden gems in {city} for a one-day tour. Include recommendations for local restaurants, landmarks, and unique experiences."
        generated_suggestions = self.huggingface_integration.generate_text(prompt)
        
        return generated_suggestions
