from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from agents.user_interaction_agent import UserInteractionAgent
from agents.itinerary_generator import ItineraryGenerator
from agents.optimization_agent import OptimizationAgent
from agents.weather_agent import WeatherAgent
from agents.memory_agent import MemoryAgent
from agents.map_generator import MapGenerator
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# Initialize Agents
user_interaction_agent = UserInteractionAgent()
itinerary_generator = ItineraryGenerator()
optimization_agent = OptimizationAgent()
weather_agent = WeatherAgent()
memory_agent = MemoryAgent()
map_generator = MapGenerator()

# Define data models for API requests
class UserPreferences(BaseModel):
    city: str
    start_time: str
    end_time: str
    budget: float
    interests: List[str]
    starting_point: Optional[str] = None

class ItineraryItem(BaseModel):
    name: str
    time: str
    transport: str
    status: Optional[str] = None

class ItineraryResponse(BaseModel):
    itinerary: List[ItineraryItem]
    optimized_route: Optional[List[ItineraryItem]] = None
    weather_info: Optional[dict] = None
    map_link: Optional[str] = None

# Endpoint to collect user preferences
@app.post("/collect_preferences")
async def collect_preferences(preferences: UserPreferences):
    try:
        # Save preferences in memory
        memory_agent.store_preferences(preferences)
        user_interaction_agent.collect_preferences(preferences)
        return {"message": "Preferences collected successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to generate an initial itinerary based on user preferences
@app.post("/generate_itinerary", response_model=ItineraryResponse)
async def generate_itinerary(preferences: UserPreferences):
    try:
        itinerary = itinerary_generator.generate_itinerary(preferences.city, preferences.interests)
        return {"itinerary": itinerary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to optimize the itinerary based on user budget and preferences
@app.post("/optimize_route", response_model=ItineraryResponse)
async def optimize_route(preferences: UserPreferences, itinerary: List[ItineraryItem]):
    try:
        optimized_route = optimization_agent.optimize_route(itinerary, preferences.budget)
        return {"optimized_route": optimized_route}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to fetch weather information for the selected city and date
@app.get("/weather")
async def get_weather(city: str, date: str):
    try:
        weather_info = weather_agent.fetch_weather(city, date)
        return {"weather_info": weather_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to generate a map based on itinerary locations
@app.post("/generate_map")
async def generate_map(locations: List[tuple]):
    try:
        map_link = map_generator.create_map(locations)
        return {"map_link": map_link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to store additional user preferences dynamically
@app.post("/store_preference")
async def store_preference(user_id: str, key: str, value: str):
    try:
        memory_agent.store_preference(user_id, key, value)
        return {"message": "Preference stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to generate a complete itinerary with weather info and map link
@app.post("/generate_complete_itinerary", response_model=ItineraryResponse)
async def generate_complete_itinerary(preferences: UserPreferences):
    try:
        # Step 1: Generate initial itinerary
        itinerary = itinerary_generator.generate_itinerary(preferences.city, preferences.interests)

        # Step 2: Optimize the route based on budget
        optimized_route = optimization_agent.optimize_route(itinerary, preferences.budget)

        # Step 3: Fetch weather information
        weather_info = weather_agent.fetch_weather(preferences.city, preferences.start_time.split(" ")[0])

        # Step 4: Generate map for the optimized route
        locations = [(item['latitude'], item['longitude']) for item in optimized_route]
        map_link = map_generator.create_map(locations)

        # Step 5: Return the complete itinerary response
        return {
            "itinerary": itinerary,
            "optimized_route": optimized_route,
            "weather_info": weather_info,
            "map_link": map_link
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
