"""
Offline Command Handler
======================
Handles commands without internet.
Local alternatives for web-dependent features.
"""

import os
import webbrowser
from core.logger import logger


class OfflineCommandHandler:
    def __init__(self, app=None):
        self.app = app

    def handle_search(self, query):
        """Offline search - open in browser when online, local file search when offline."""
        if self._is_online():
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching Google for: {query}", "english"
        else:
            return self._local_search(query)

    def handle_youtube(self, query):
        """Offline YouTube - open in browser when online."""
        if self._is_online():
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Searching YouTube for: {query}", "english"
        else:
            return "YouTube requires internet. I can play local music instead.", "english"

    def handle_wikipedia(self, query):
        """Offline Wikipedia - local knowledge when offline."""
        if self._is_online():
            try:
                import wikipedia
                result = wikipedia.summary(query, sentences=2)
                return result, "english"
            except:
                return f"Could not find Wikipedia article for: {query}", "english"
        else:
            return self._local_knowledge(query)

    def handle_weather(self, city=""):
        """Offline weather - cached or message."""
        if self._is_online():
            try:
                import requests
                url = f"https://wttr.in/{city}?format=3"
                response = requests.get(url, timeout=5)
                return response.text, "english"
            except:
                return "Could not fetch weather", "english"
        else:
            return "Weather requires internet. Check your local weather app.", "english"

    def handle_news(self):
        """Offline news."""
        if self._is_online():
            webbrowser.open("https://news.google.com")
            return "Opening Google News", "english"
        else:
            return "News requires internet.", "english"

    def _local_search(self, query):
        """Search local files."""
        search_dirs = [
            os.path.expanduser("~\\Documents"),
            os.path.expanduser("~\\Desktop"),
            os.path.expanduser("~\\Downloads"),
        ]

        results = []
        query_lower = query.lower()

        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
            try:
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        if query_lower in file.lower():
                            results.append(os.path.join(root, file))
                            if len(results) >= 5:
                                break
                    if len(results) >= 5:
                        break
            except:
                continue

        if results:
            response = f"Found {len(results)} local files:\n"
            for r in results[:5]:
                response += f"- {os.path.basename(r)}\n"
            return response, "english"
        else:
            return f"No local files found matching: {query}", "english"

    def _local_knowledge(self, topic):
        """Provide basic local knowledge."""
        knowledge = {
            "python": "Python is a programming language created by Guido van Rossum in 1991.",
            "javascript": "JavaScript is a programming language for web development.",
            "html": "HTML is a markup language for creating web pages.",
            "css": "CSS is a styling language for web pages.",
            "java": "Java is a programming language by Sun Microsystems.",
            "windows": "Windows is an operating system by Microsoft.",
            "linux": "Linux is an open-source operating system.",
            "ai": "Artificial Intelligence is computer simulation of human intelligence.",
            "machine learning": "Machine Learning is a subset of AI that learns from data.",
        }

        topic_lower = topic.lower()
        for key, value in knowledge.items():
            if key in topic_lower:
                return value, "english"

        return f"Local knowledge not available for: {topic}. Try connecting to internet.", "english"

    def _is_online(self):
        """Check if internet is available."""
        try:
            import requests
            requests.get("https://www.google.com", timeout=2)
            return True
        except:
            return False

    def get_status(self):
        """Get offline/online status."""
        online = self._is_online()
        return "Online" if online else "Offline (using local features)"
