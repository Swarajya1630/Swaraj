"""
Task Automation Module
======================
Handles real-world actions like opening apps, searching web, time, etc.
Supports commands in English, Hindi, and Marathi.
"""

import os
import webbrowser
import subprocess
import datetime
import wikipedia


class TaskAutomation:
    def __init__(self):
        # Windows Store apps use "shell:AppsFolder\Microsoft.AppID" format
        self.applications = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "file explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "terminal": "wt.exe",
            "vscode": r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
        }

        # Windows Store apps - use start command with app name
        self.store_apps = {
            "whatsapp": "whatsapp:",
            "spotify": "spotify:",
            "youtube": "https://www.youtube.com",
            "teams": "ms-teams:",
            "outlook": "outlook:",
            "photos": "ms-photos:",
            "maps": "bingmaps:",
            "settings": "ms-settings:",
            "store": "ms-windows-store:",
        }

        # Multilingual command keywords
        self.keywords = {
            "open": ["open", "उघडा", "खोला", "उघड"],
            "search": ["search", "शोधा", "खोजो", "शोध"],
            "play": ["play", "चालवा", "चलाओ"],
            "time": ["time", "वेळ", "समय", "time काय आहे", "time बताओ"],
            "date": ["date", "तारीख", "आज", "date काय आहे"],
            "wikipedia": ["wikipedia", "विकिपीडिया"],
            "who is": ["who is", "कोण आहे", "कौन है"],
            "what is": ["what is", "काय आहे", "क्या है"],
            "system": ["system", "सिस्टम"],
            "exit": ["exit", "quit", "bye", "बाहेर", "बंद"],
        }

    def open_application(self, app_name):
        app_name_lower = app_name.lower().strip()

        # Try regular desktop apps first
        if app_name_lower in self.applications:
            path = self.applications[app_name_lower]
            path = path.replace("{user}", os.getlogin())
            try:
                subprocess.Popen(path)
                return f"Opening {app_name}."
            except FileNotFoundError:
                pass

        # Try Windows Store apps (whatsapp, spotify, etc.)
        if app_name_lower in self.store_apps:
            try:
                os.system(f"start {self.store_apps[app_name_lower]}")
                return f"Opening {app_name}."
            except Exception:
                pass

        # Try as a direct command
        try:
            subprocess.Popen(f"start {app_name}", shell=True)
            return f"Trying to open {app_name}."
        except Exception as e:
            return f"Could not open {app_name}. Error: {str(e)}"

    def search_web(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching Google for: {query}"

    def search_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return f"Searching YouTube for: {query}"

    def play_on_spotify(self, query):
        """Open Spotify web player with search."""
        url = f"https://open.spotify.com/search/{query}"
        webbrowser.open(url)
        return f"Playing {query} on Spotify."

    def open_website(self, website):
        if not website.startswith("http"):
            website = f"https://www.{website}"
        webbrowser.open(website)
        return f"Opening {website}"

    def get_time(self, language="english"):
        now = datetime.datetime.now()
        if language == "hindi":
            return now.strftime("अभी %I:%M %p बज रहे हैं")
        elif language == "marathi":
            return now.strftime("आता %I:%M %p वाजत आहेत")
        return now.strftime("It's %I:%M %p")

    def get_date(self, language="english"):
        now = datetime.datetime.now()
        if language == "hindi":
            return now.strftime("आज %B %d, %Y है")
        elif language == "marathi":
            return now.strftime("आज %B %d, %Y आहे")
        return now.strftime("Today is %B %d, %Y")

    def wikipedia_search(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Did you mean: {', '.join(e.options[:3])}?"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia article found for '{query}'."

    def system_info(self):
        import platform
        system = platform.system()
        node = platform.node()
        return f"Running on {system}, machine name: {node}"

    def _check_keywords(self, text, keyword_group):
        text_lower = text.lower()
        for kw in self.keywords.get(keyword_group, []):
            if kw in text_lower:
                return True
        return False

    def get_weather(self, city="auto"):
        """Get current weather."""
        try:
            from weather import Weather
            w = Weather(city)
            data = w.get_weather(city)
            return f"Weather in {data['city']}: {data['temp_c']}°C, {data['condition']}. Humidity: {data['humidity']}%, Wind: {data['wind_speed']}km/h"
        except Exception as e:
            return f"Couldn't fetch weather: {str(e)}"

    def execute_command(self, text, language="english"):
        text_lower = text.lower()

        # --- Weather ---
        if "weather" in text_lower or "मौसम" in text_lower or "हवामान" in text_lower:
            city = "auto"
            if " in " in text_lower:
                city = text_lower.split(" in ")[-1].strip()
            return self.get_weather(city)

        # --- Play on Spotify ---
        if self._check_keywords(text, "play") and "spotify" in text_lower:
            query = text_lower
            for kw in self.keywords["play"] + ["spotify", "on", "play"]:
                query = query.replace(kw, "")
            return self.play_on_spotify(query.strip())

        # --- App Opening ---
        if self._check_keywords(text, "open"):
            app = text_lower
            for kw in self.keywords["open"]:
                app = app.replace(kw, "")
            return self.open_application(app.strip())

        # --- Web Search ---
        elif self._check_keywords(text, "search") and "youtube" in text_lower:
            query = text_lower
            for kw in self.keywords["search"] + ["youtube", "for"]:
                query = query.replace(kw, "")
            return self.search_youtube(query.strip())

        elif self._check_keywords(text, "search"):
            query = text_lower
            for kw in self.keywords["search"] + ["for"]:
                query = query.replace(kw, "")
            return self.search_web(query.strip())

        # --- YouTube ---
        elif self._check_keywords(text, "play") and "youtube" in text_lower:
            query = text_lower
            for kw in self.keywords["play"] + ["youtube", "on"]:
                query = query.replace(kw, "")
            return self.search_youtube(query.strip())

        # --- Wikipedia ---
        elif self._check_keywords(text, "wikipedia") or \
             self._check_keywords(text, "who is") or \
             self._check_keywords(text, "what is"):
            query = text_lower
            for kw in self.keywords["wikipedia"] + self.keywords["who is"] + self.keywords["what is"]:
                query = query.replace(kw, "")
            return self.wikipedia_search(query.strip())

        # --- Time ---
        elif self._check_keywords(text, "time"):
            return self.get_time(language)

        # --- Date ---
        elif self._check_keywords(text, "date"):
            return self.get_date(language)

        # --- Website ---
        elif ".com" in text_lower or ".org" in text_lower or ".net" in text_lower:
            return self.open_website(text_lower)

        # --- System Info ---
        elif self._check_keywords(text, "system"):
            return self.system_info()

        # --- No Match ---
        else:
            return None
