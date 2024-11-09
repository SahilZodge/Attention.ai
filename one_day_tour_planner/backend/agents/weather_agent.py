import requests
from datetime import datetime

class WeatherAgent:
    def __init__(self, api_key: str):
        # Initialize with an API key for the weather service
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def fetch_weather(self, city: str, date: str) -> dict:
        """
        Fetches weather forecast data for a specific city and date.
        
        Args:
            city (str): The name of the city for which to fetch the weather forecast.
            date (str): The date for the forecast in 'YYYY-MM-DD' format.

        Returns:
            dict: A dictionary with weather details like temperature, conditions, and recommendations.
        """
        # Request weather data from the OpenWeatherMap API
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Metric units (Celsius) for temperature
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an error for HTTP issues
            forecast_data = response.json()

            # Extract relevant weather data for the requested date
            daily_weather = self.extract_weather_for_date(forecast_data, date)
            return daily_weather
        
        except requests.RequestException as e:
            return {"error": f"Failed to retrieve weather data: {str(e)}"}

    def extract_weather_for_date(self, forecast_data: dict, date: str) -> dict:
        """
        Extracts and formats weather data for a specific date from forecast data.

        Args:
            forecast_data (dict): The full forecast data returned from the API.
            date (str): The target date in 'YYYY-MM-DD' format.

        Returns:
            dict: Processed weather information for the specified date.
        """
        target_day_data = [
            item for item in forecast_data['list'] if item['dt_txt'].startswith(date)
        ]

        # Process data to find the average temperature and main weather conditions
        temperatures = [entry['main']['temp'] for entry in target_day_data]
        conditions = [entry['weather'][0]['description'] for entry in target_day_data]

        # Calculate average temperature and find the most common weather condition
        avg_temp = sum(temperatures) / len(temperatures) if temperatures else None
        main_condition = max(set(conditions), key=conditions.count) if conditions else "unknown"

        # Construct a user-friendly weather summary
        weather_summary = {
            "date": date,
            "average_temperature": avg_temp,
            "condition": main_condition,
            "recommendation": self.get_weather_recommendation(main_condition)
        }
        return weather_summary

    def get_weather_recommendation(self, condition: str) -> str:
        """
        Provides a recommendation based on the weather condition.

        Args:
            condition (str): The weather condition (e.g., "rain", "clear sky").

        Returns:
            str: A recommendation for the user based on the weather.
        """
        if "rain" in condition:
            return "It's likely to rain. Bring an umbrella or consider indoor activities."
        elif "clear" in condition:
            return "The weather is clear. It's a great day for outdoor activities!"
        elif "snow" in condition:
            return "Snow is expected. Dress warmly and consider indoor activities."
        elif "cloud" in condition:
            return "It's cloudy. You may want to prepare for mixed weather."
        elif "storm" in condition:
            return "A storm is expected. Stay indoors and avoid outdoor activities."
        else:
            return "Check the forecast closer to your trip for specific recommendations."

