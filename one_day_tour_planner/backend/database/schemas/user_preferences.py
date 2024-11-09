from pydantic import BaseModel, Field
from typing import List

class UserPreferences(BaseModel):
    """
    This model represents the preferences of a user. It is used to validate the
    data structure for storing and processing user preferences related to
    their travel or activities.

    Attributes:
        city (str): The city the user wants to visit or is interested in.
        start_time (str): The start time for the user's desired activity or trip in ISO format (YYYY-MM-DDTHH:MM:SS).
        end_time (str): The end time for the user's desired activity or trip in ISO format (YYYY-MM-DDTHH:MM:SS).
        budget (float): The maximum budget the user has allocated for the activity or trip.
        interests (List[str]): A list of interests or activities the user is interested in, like "culture", "adventure", "food".
    """
    
    city: str = Field(..., title="City Name", description="The name of the city the user is interested in.")
    start_time: str = Field(..., title="Start Time", description="The start time of the user's trip or activity in ISO format.")
    end_time: str = Field(..., title="End Time", description="The end time of the user's trip or activity in ISO format.")
    budget: float = Field(..., title="Budget", description="The user's budget for the activity or trip.")
    interests: List[str] = Field(..., title="User Interests", description="A list of interests or activities that the user is interested in.")
    
    class Config:
        # Ensuring that Pydantic will work well with the data in a schema-like fashion
        anystr_strip_whitespace = True  # Strips leading and trailing spaces from strings
        min_anystr_length = 1  # Ensures string fields have at least one character
        max_anystr_length = 255  # Ensures string fields are not too long
    
    def __str__(self):
        return f"User Preferences for {self.city} from {self.start_time} to {self.end_time} with a budget of {self.budget}"
    
    def __repr__(self):
        return f"UserPreferences(city={self.city}, start_time={self.start_time}, end_time={self.end_time}, budget={self.budget}, interests={self.interests})"
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a UserPreferences instance from a dictionary.
        
        Args:
            data (dict): A dictionary with keys matching the model's attributes.
        
        Returns:
            UserPreferences: A Pydantic model instance.
        """
        return cls(**data)
