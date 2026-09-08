"""
Web Search Commands
==================
Google, YouTube, Wikipedia, weather searches.
"""

import webbrowser
import re
from core.logger import logger


class WebSearchCommand:
    def __init__(self, app=None):
        self.app = app

    def execute(self, action, text):
        if action == "search":
            return self._web_search(text)
        elif action == "wiki":
            return self._wikipedia_search(text)
        elif action == "weather":
            return self._weather_search(text)
        return "Unknown search command.", "english"

    def _web_search(self, text):
        text_lower = text.lower()
        query = text_lower

        for word in ["search", "शोध", "खोज", "google", "youtube", "web", "internet", "for", "on", "में", "पर", "वर"]:
            query = query.replace(word, "").strip()

        if not query:
            return "What would you like me to search for?", "english"

        if "youtube" in text_lower:
            try:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                return f"Searching YouTube for {query}.", "english"
            except Exception as e:
                return "Couldn't open YouTube.", "english"
        else:
            try:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return f"Searching Google for {query}.", "english"
            except Exception as e:
                return "Couldn't open Google.", "english"

    def _wikipedia_search(self, text):
        text_lower = text.lower()
        query = text_lower

        for word in ["what is", "who is", "क्या है", "कौन है", "काय आहे", "कोण आहे",
                      "tell me about", "बताओ", "सांगा", "wikipedia", "विकिपीडिया"]:
            query = query.replace(word, "").strip()

        if not query:
            return "What would you like to know about?", "english"

        try:
            import wikipedia
            result = wikipedia.summary(query, sentences=2)
            return result, "english"
        except wikipedia.exceptions.DisambiguationError as e:
            options = ", ".join(e.options[:3])
            return f"Multiple results found. Did you mean: {options}?", "english"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia article found for '{query}'.", "english"
        except Exception as e:
            return f"Couldn't search Wikipedia.", "english"

    def _weather_search(self, text):
        text_lower = text.lower()
        city = "auto"

        patterns = [
            r"weather (?:in|at|of) (\w+)",
            r"मौसम (\w+)",
            r"हवामान (\w+)",
            r"weather (\w+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                city = match.group(1)
                break

        try:
            import requests
            if city == "auto":
                response = requests.get("https://wttr.in/?format=j1", timeout=10)
            else:
                response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)

            data = response.json()
            current = data["current_condition"][0]
            area = data["nearest_area"][0]

            temp = current["temp_C"]
            condition = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind = current["windspeedKmph"]
            location = area["areaName"][0]["value"]

            return f"Weather in {location}: {temp}°C, {condition}. Humidity: {humidity}%, Wind: {wind}km/h.", "english"
        except Exception as e:
            return "Couldn't fetch weather right now.", "english"
