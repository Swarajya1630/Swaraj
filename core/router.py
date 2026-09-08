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

        self._camera_patterns = [
            (r"\b(take|capture)\b.*\b(screenshot|photo|picture)\b", "screenshot"),
            (r"\b(detect|find|scan)\b.*\b(face|faces)\b", "faces"),
            (r"\b(scan|read)\b.*\b(qr|code|barcode)\b", "qr"),
            (r"\b(camera|webcam)\b.*\b(info|status)\b", "info"),
        ]

        self._calendar_patterns = [
            (r"\b(add|create|schedule)\b.*\b(event|meeting|appointment)\b", "add_event"),
            (r"\b(show|list|what)\b.*\b(events|calendar|schedule)\b", "list_events"),
            (r"\b(upcoming|next)\b.*\b(events|meetings)\b", "upcoming"),
            (r"\b(add|create)\b.*\b(contact|person)\b", "add_contact"),
            (r"\b(find|search)\b.*\b(contact|person)\b", "find_contact"),
        ]

        self._wake_patterns = [
            (r"\b(add|create|train)\b.*\b(wake word|activation phrase)\b", "add_wake"),
            (r"\b(list|show)\b.*\b(wake words|activation phrases)\b", "list_wake"),
            (r"\b(remove|delete)\b.*\b(wake word)\b", "remove_wake"),
        ]

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

        camera_result = self._check_camera(text_lower)
        if camera_result:
            return camera_result

        calendar_result = self._check_calendar(text_lower)
        if calendar_result:
            return calendar_result

        wake_result = self._check_wake_training(text_lower)
        if wake_result:
            return wake_result

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

    def _check_camera(self, text):
        """Check for camera commands."""
        if not self.app or not hasattr(self.app, 'camera') or not self.app.camera:
            return None

        for pattern, action in self._camera_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if action == "screenshot":
                    filepath, msg = self.app.camera.take_screenshot()
                    return msg, "english"
                elif action == "faces":
                    filepath, msg = self.app.camera.detect_faces()
                    return msg, "english"
                elif action == "qr":
                    data, msg = self.app.camera.scan_qr()
                    return msg, "english"
                elif action == "info":
                    return self.app.camera.get_camera_info(), "english"
        return None

    def _check_calendar(self, text):
        """Check for calendar commands."""
        if not self.app or not hasattr(self.app, 'email_calendar') or not self.app.email_calendar:
            return None

        for pattern, action in self._calendar_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if action == "list_events":
                    events = self.app.email_calendar.get_events()
                    return self.app.email_calendar.format_events(events), "english"
                elif action == "upcoming":
                    events = self.app.email_calendar.get_upcoming(7)
                    return self.app.email_calendar.format_events(events), "english"
                elif action == "add_event":
                    return "To add an event, say: 'add event meeting with team on 2024-01-15 at 10:00'", "english"
                elif action == "add_contact":
                    return "To add a contact, say: 'add contact John with email john@example.com'", "english"
                elif action == "find_contact":
                    return "To find a contact, say: 'find contact John'", "english"
        return None

    def _check_wake_training(self, text):
        """Check for wake word training commands."""
        if not self.app or not hasattr(self.app, 'wake_trainer') or not self.app.wake_trainer:
            return None

        for pattern, action in self._wake_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if action == "list_wake":
                    words = self.app.wake_trainer.list_wake_words()
                    if not words:
                        return "No custom wake words configured. Default: 'Hey Swaraj', 'Swaraj'", "english"
                    phrases = [w["phrase"] for w in words]
                    return f"Custom wake words: {', '.join(phrases)}", "english"
                elif action == "add_wake":
                    return "To add a wake word, say: 'add wake word hello assistant'", "english"
                elif action == "remove_wake":
                    return "To remove a wake word, say: 'remove wake word hello assistant'", "english"
        return None

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
