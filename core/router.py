"""
Command Router
==============
Routes user commands to appropriate handlers.
Uses intent detection for natural language commands.
"""

import re
from core.logger import logger


class CommandRouter:
    def __init__(self, app=None):
        self.app = app
        self.handlers = {}
        self.learning = None
        self._register_default_handlers()
        self._init_learning()

    def _register_default_handlers(self):
        from commands.app_control import AppControlCommand
        from commands.system_control import SystemControlCommand
        from commands.media_control import MediaControlCommand
        from commands.web_search import WebSearchCommand
        from commands.productivity import ProductivityCommand

        self.register("app", AppControlCommand(self.app))
        self.register("system", SystemControlCommand(self.app))
        self.register("media", MediaControlCommand(self.app))
        self.register("web", WebSearchCommand(self.app))
        self.register("productivity", ProductivityCommand(self.app))

    def _init_learning(self):
        try:
            from core.learning import LearningSystem
            self.learning = LearningSystem()
        except Exception as e:
            logger.warning(f"Learning system init failed: {e}")

    def register(self, category, handler):
        self.handlers[category] = handler

    def route(self, text):
        """Route a command to the appropriate handler."""
        text_lower = text.lower().strip()

        if self.learning:
            learning_response = self.learning.check(text)
            if learning_response:
                return learning_response, "english"

        intent = self._detect_intent(text_lower)

        if intent:
            category, action = intent
            handler = self.handlers.get(category)
            if handler:
                logger.debug(f"Routing to {category}.{action}: {text}")
                return handler.execute(action, text)

        if self.app and self.app.ai_brain:
            response, lang = self.app.ai_brain.think(text)
            return response, lang

        return "I'm not sure how to help with that. Try saying 'open Chrome' or 'what time is it'.", "english"

    def _detect_intent(self, text):
        """Detect the intent from user text."""
        patterns = [
            (r"\b(open|launch|start|run|भरा|उघड)\b.*\b(chrome|firefox|vscode|notepad|spotify|whatsapp|calculator|explorer|terminal|cmd|word|excel|powerpoint)\b", "app", "open"),
            (r"\b(close|quit|exit|band|बंद)\b.*\b(chrome|firefox|vscode|notepad|spotify|whatsapp)\b", "app", "close"),
            (r"\b(open|go to|show|visit)\b.*\b(downloads|documents|desktop|pictures|music|videos)\b", "app", "folder"),
            (r"\b(open|go to|show|visit)\b.*\bmy project|project folder|project directory\b", "app", "folder"),
            (r"\b(what time|time|वेळ|समय|time क्या)\b", "system", "time"),
            (r"\b(what date|date|तारीख|आज|date क्या)\b", "system", "date"),
            (r"\b(system status|system info|pc status|computer status|सिस्टम)\b", "system", "status"),
            (r"\b(shutdown|restart|sleep|hibernate|lock|logout)\b", "system", "power"),
            (r"\b(volume up|volume down|mute|unmute|आवाज़|आवाज)\b", "media", "volume"),
            (r"\b(play|pause|stop|next|previous|गाना|म्यूजिक)\b", "media", "playback"),
            (r"\b(play|चालवा)\b.*\b(spotify|youtube|music|गाना)\b", "media", "play"),
            (r"\b(search|शोध|खोज)\b.*\b(google|youtube|web|internet)\b", "web", "search"),
            (r"\b(what is|who is|क्या है|कौन है|काय आहे)\b", "web", "wiki"),
            (r"\b(remind|reminder|याद|आठवण)\b", "productivity", "remind"),
            (r"\b(note|save|लिख|नोंद)\b", "productivity", "note"),
            (r"\b(weather|मौसम|हवामान)\b", "web", "weather"),
            (r"\b(show me|tell me|बताओ|सांगा)\b.*\b(weather|time|date|status)\b", "system", "info"),
        ]

        for pattern, category, action in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return category, action

        return None
