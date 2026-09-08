"""
Weather Module
==============
Fetches live weather data from wttr.in (free, no API key).
Shows temperature, humidity, wind, and conditions.
"""

import requests
import json


class Weather:
    def __init__(self, city="auto"):
        self.city = city
        self.cache = None
        self.cache_time = 0

    def get_weather(self, city=None):
        """Get current weather for a city."""
        if city:
            self.city = city

        try:
            url = f"https://wttr.in/{self.city}?format=j1"
            response = requests.get(url, timeout=10)
            data = response.json()

            current = data["current_condition"][0]
            area = data["nearest_area"][0]

            weather = {
                "city": area["areaName"][0]["value"],
                "country": area["country"][0]["value"],
                "temp_c": current["temp_C"],
                "temp_f": current["temp_F"],
                "feels_like": current["FeelsLikeC"],
                "humidity": current["humidity"],
                "wind_speed": current["windspeedKmph"],
                "wind_dir": current["winddir16Point"],
                "condition": current["weatherDesc"][0]["value"].strip(),
                "visibility": current["visibility"],
                "uv_index": current["uvIndex"],
                "pressure": current["pressure"],
                "sunrise": data["weather"][0]["astronomy"][0]["sunrise"],
                "sunset": data["weather"][0]["astronomy"][0]["sunset"],
            }

            self.cache = weather
            return weather

        except Exception as e:
            return {
                "city": "Unknown",
                "temp_c": "--",
                "condition": "Unable to fetch",
                "humidity": "--",
                "wind_speed": "--",
                "error": str(e)
            }

    def get_weather_emoji(self, condition):
        """Get emoji for weather condition."""
        condition_lower = condition.lower()
        if "sun" in condition_lower or "clear" in condition_lower:
            return "☀️"
        elif "cloud" in condition_lower or "overcast" in condition_lower:
            return "☁️"
        elif "rain" in condition_lower or "drizzle" in condition_lower:
            return "🌧️"
        elif "thunder" in condition_lower or "storm" in condition_lower:
            return "⛈️"
        elif "snow" in condition_lower:
            return "❄️"
        elif "fog" in condition_lower or "mist" in condition_lower:
            return "🌫️"
        elif "wind" in condition_lower:
            return "💨"
        else:
            return "🌤️"

    def format_display(self, weather=None):
        """Format weather for UI display."""
        if not weather:
            weather = self.cache or self.get_weather()

        emoji = self.get_weather_emoji(weather.get("condition", ""))

        return {
            "main": f"{emoji} {weather.get('temp_c', '--')}°C",
            "condition": weather.get("condition", "Unknown"),
            "details": f"H:{weather.get('humidity', '--')}% W:{weather.get('wind_speed', '--')}km/h",
            "city": weather.get("city", "Unknown"),
            "feels_like": f"Feels like {weather.get('feels_like', '--')}°C"
        }


if __name__ == "__main__":
    w = Weather()
    data = w.get_weather("Bangalore")
    print(json.dumps(data, indent=2))
