from typing import List, Dict
from datetime import datetime, timedelta

# Sample database of attractions for demonstration
# In a real application, this could be replaced with a dynamic database query or API call
attractions_db = {
    "Rome": [
        {"name": "Colosseum", "category": "historical", "duration": 90, "cost": 15},
        {"name": "Roman Forum", "category": "historical", "duration": 75, "cost": 12},
        {"name": "Pantheon", "category": "historical", "duration": 45, "cost": 0},
        {"name": "Piazza Navona", "category": "food", "duration": 60, "cost": 0},
        {"name": "Trevi Fountain", "category": "relaxing", "duration": 30, "cost": 0},
        {"name": "Spanish Steps", "category": "relaxing", "duration": 45, "cost": 0}
    ],
    "Paris": [
        {"name": "Eiffel Tower", "category": "historical", "duration": 120, "cost": 25},
        {"name": "Louvre Museum", "category": "historical", "duration": 180, "cost": 20},
        {"name": "Montmartre", "category": "shopping", "duration": 60, "cost": 0},
        {"name": "Notre Dame", "category": "historical", "duration": 60, "cost": 0},
        {"name": "Seine River Cruise", "category": "relaxing", "duration": 90, "cost": 15}
    ]
}

class ItineraryGenerator:
    def generate_itinerary(self, city: str, interests: List[str], start_time: str) -> List[Dict]:
        """
        Generates an itinerary based on the selected city, user interests, and start time.
        """
        if city not in attractions_db:
            return [{"error": f"No data available for city: {city}"}]

        # Filter attractions by user interests
        relevant_attractions = self.filter_attractions(city, interests)
        
        # Sort attractions by category preference and optimize the order
        optimized_itinerary = self.create_optimized_itinerary(relevant_attractions, start_time)
        
        return optimized_itinerary

    def filter_attractions(self, city: str, interests: List[str]) -> List[Dict]:
        """
        Filters attractions in the specified city based on user interests.
        """
        attractions = attractions_db[city]
        filtered_attractions = [
            attraction for attraction in attractions if attraction['category'] in interests
        ]
        return filtered_attractions

    def create_optimized_itinerary(self, attractions: List[Dict], start_time: str) -> List[Dict]:
        """
        Organizes the itinerary by calculating start and end times for each attraction.
        """
        itinerary = []
        current_time = datetime.strptime(start_time, "%H:%M")

        for attraction in attractions:
            start_time_str = current_time.strftime("%I:%M %p")
            end_time = current_time + timedelta(minutes=attraction["duration"])
            end_time_str = end_time.strftime("%I:%M %p")
            
            itinerary.append({
                "name": attraction["name"],
                "category": attraction["category"],
                "start_time": start_time_str,
                "end_time": end_time_str,
                "duration": attraction["duration"],
                "cost": attraction["cost"]
            })

            # Update the current time to the end of this attraction visit
            current_time = end_time + timedelta(minutes=15)  # 15 minutes buffer time between stops

        return itinerary
