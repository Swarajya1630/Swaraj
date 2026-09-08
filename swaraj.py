"""
S.W.A.R.A.J - Smart Wide-purpose Automated Reasoning And Assistance Junction
==============================================================================
Your personal AI best friend. Only YOU (Shiva) can talk to it.

Usage:
    python swaraj.py                    # Normal mode
    python swaraj.py --text             # Text mode
    python swaraj.py --ui               # Jarvis GUI with Rajmudra
    python swaraj.py --setup            # First-time setup
    python swaraj.py --voice            # Voice commands (no wake word)
    python swaraj.py --lang hindi       # Hindi mode
    python swaraj.py --lang marathi     # Marathi mode
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from listener import SpeechRecognizer
from speaker import Speaker
from ai_brain import AIBrain
from task_automation import TaskAutomation
from wake_word import WakeWordDetector
from identity import PersonalIdentity


class Swaraj:
    def __init__(self, use_ai=True, language="english"):
        print("Initializing SWARAJ...")

        self.speaker = Speaker(rate=175, volume=0.9)
        self.recognizer = SpeechRecognizer()
        self.automation = TaskAutomation()
        self.wake_detector = WakeWordDetector()
        self.identity = PersonalIdentity()
        self.current_language = language.lower()

        self.recognizer.set_language(self.current_language)

        self.ai = None
        if use_ai:
            try:
                self.ai = AIBrain(model="mistral")
                self.ai.set_language(self.current_language)
                print("AI Brain connected (Ollama - mistral)")
            except Exception as e:
                print(f"AI Brain offline: {e}")
                print("Running in basic mode (task automation only)")

    def setup_mode(self):
        """First-time setup."""
        print("\n" + "="*50)
        print("   SWARAJ - FIRST TIME SETUP")
        print("="*50)

        if self.identity.data["owner"]["is_trained"]:
            print(f"\nOwner registered: {self.identity.get_owner_name()}")
            choice = input("Do you want to retrain? (yes/no): ").lower()
            if choice != "yes":
                print("Setup cancelled.")
                return

        print("\nHey! I'm Swaraj. Let's become best friends!\n")

        name = input("What's your name? ").strip()
        if not name:
            name = "Shiva"

        nickname = input("What should I call you? (default: shiva): ").strip()
        if not nickname:
            nickname = "shiva"

        self.identity.setup_owner(name, nickname)

        print(f"\nNice to meet you, {name}! Tell me more:\n")

        age = input("Your age: ").strip()
        if age: self.identity.learn_fact("age", age)

        city = input("Your city: ").strip()
        if city: self.identity.learn_fact("city", city)

        hobby = input("Favorite hobby: ").strip()
        if hobby: self.identity.learn_fact("hobby", hobby)

        music = input("Favorite music/artist: ").strip()
        if music: self.identity.learn_fact("music", music)

        food = input("Favorite food: ").strip()
        if food: self.identity.learn_fact("food", food)

        goal = input("Current goal/dream: ").strip()
        if goal: self.identity.learn_fact("goal", goal)

        print(f"\nPersonality (1-10, Enter for default):\n")

        humor = input("Humor (1=serious, 10=very funny): ").strip()
        if humor and humor.isdigit():
            self.identity.set_personality_trait("humor", int(humor) / 10)

        sarcasm = input("Sarcasm (1=none, 10=very sarcastic): ").strip()
        if sarcasm and sarcasm.isdigit():
            self.identity.set_personality_trait("sarcasm_level", int(sarcasm) / 10)

        print("\n" + "="*50)
        print(f"   All set, {name}! We're best friends now!")
        print(f"   I'll call you: {nickname}")
        print(f"   Only YOU can talk to me.")
        print("="*50)
        print("\nNow run: python swaraj.py --text")

    def _detect_language_switch(self, text):
        text_lower = text.lower()
        for lang in ["english", "hindi", "marathi", "इंग्रजी", "हिंदी", "मराठी",
                      "अंग्रेजी", "हिंदी", "मराठी"]:
            if lang in text_lower:
                lang_map = {
                    "english": "english", "इंग्रजी": "english", "अंग्रेजी": "english",
                    "hindi": "hindi", "हिंदी": "hindi",
                    "marathi": "marathi", "मराठी": "marathi"
                }
                if lang in lang_map:
                    return lang_map[lang]
        return None

    def _detect_bookmark_command(self, text):
        """Detect bookmark save/open/list/remove commands."""
        text_lower = text.lower()

        # Save bookmark: "save website youtube.com as youtube"
        if "save" in text_lower and ("website" in text_lower or "link" in text_lower or "url" in text_lower):
            return "save"

        # Open bookmark: "open youtube"
        if "open" in text_lower:
            # Check if it's a saved bookmark
            app = text_lower.replace("open", "").strip()
            bookmark_url = self.identity.get_bookmark(app)
            if bookmark_url:
                return "open_bookmark"

        # List bookmarks
        if "list" in text_lower and ("bookmark" in text_lower or "website" in text_lower or "link" in text_lower):
            return "list"

        # Remove bookmark
        if "remove" in text_lower and ("bookmark" in text_lower or "website" in text_lower):
            return "remove"

        return None

    def _handle_bookmark(self, text):
        """Handle bookmark operations."""
        text_lower = text.lower()
        action = self._detect_bookmark_command(text)

        if action == "save":
            # Parse: "save website youtube.com as youtube"
            try:
                if " as " in text_lower:
                    parts = text_lower.split(" as ")
                    url_part = parts[0].replace("save", "").replace("website", "").replace("link", "").replace("url", "").strip()
                    name = parts[1].strip()
                elif " link " in text_lower:
                    parts = text_lower.split(" link ")
                    name = parts[0].replace("save", "").replace("website", "").strip()
                    url_part = parts[1].strip()
                else:
                    return "Format: save website <url> as <name>", self.current_language

                self.identity.add_bookmark(name, url_part)
                return f"Saved! Say 'open {name}' anytime to go there.", self.current_language
            except:
                return "Couldn't save. Use: save website <url> as <name>", self.current_language

        elif action == "open_bookmark":
            import webbrowser
            app = text_lower.replace("open", "").strip()
            url = self.identity.get_bookmark(app)
            if url:
                webbrowser.open(url)
                return f"Opening {app}.", self.current_language

        elif action == "list":
            bookmarks = self.identity.list_bookmarks()
            if bookmarks:
                lines = ["Your saved websites:"]
                for name, url in bookmarks.items():
                    lines.append(f"  {name} -> {url}")
                return "\n".join(lines), self.current_language
            else:
                return "No bookmarks saved yet. Use: save website <url> as <name>", self.current_language

        elif action == "remove":
            # Extract name to remove
            for word in ["remove", "bookmark", "website", "link"]:
                text_lower = text_lower.replace(word, "")
            name = text_lower.strip()
            if self.identity.remove_bookmark(name):
                return f"Removed bookmark: {name}", self.current_language
            else:
                return f"Bookmark '{name}' not found.", self.current_language

        return None, self.current_language

    def _detect_learning(self, text):
        text_lower = text.lower()
        learn_patterns = [
            "remember that", "yaad rakh", "ले", "सेव्ह कर",
            "my favorite", "माझं आवडतं", "मेरा पसंदीदा",
            "i like", "i love", "मला आवडते", "मुझे पसंद है",
            "i hate", "मला नावडते", "मुझे नफरत है"
        ]
        for pattern in learn_patterns:
            if pattern in text_lower:
                return True
        return False

    def process_command(self, text):
        text_lower = text.lower().strip()

        # --- Exit Commands ---
        exit_words = ["exit", "quit", "bye", "goodbye", "shutdown",
                       "बाहेर", "बंद", "अलविदा", "बंद कर"]
        if any(word in text_lower for word in exit_words):
            nickname = self.identity.get_random_nickname()
            return f"See you later, {nickname}! I'll be here waiting.", self.current_language

        # --- Language Switch ---
        new_lang = self._detect_language_switch(text)
        if new_lang and ("switch" in text_lower or "बदल" in text_lower or
                         "set" in text_lower or "change" in text_lower or
                         new_lang in text_lower):
            self.current_language = new_lang
            self.recognizer.set_language(new_lang)
            if self.ai:
                self.ai.set_language(new_lang)
            responses = {
                "english": "Language switched to English!",
                "hindi": "भाषा हिंदी में बदल दी गई!",
                "marathi": "भाषा मराठीत बदलली!"
            }
            return responses[new_lang], new_lang

        # --- Clear History ---
        if "clear history" in text_lower or "नया" in text_lower:
            if self.ai:
                self.ai.clear_history()
            return "Fresh start! What's on your mind?", self.current_language

        # --- Friendship Stats ---
        if "friendship" in text_lower or "level" in text_lower or "stats" in text_lower:
            level = self.identity.data["friendship"]["level"]
            xp = self.identity.data["friendship"]["xp"]
            convos = self.identity.data["friendship"]["total_conversations"]
            return (f"Friendship Level: {level} | XP: {xp} | "
                    f"Conversations: {convos}. We're getting closer!"), self.current_language

        # --- Bookmark Commands ---
        if self._detect_bookmark_command(text):
            result, lang = self._handle_bookmark(text)
            if result:
                return result, lang

        # --- Teach Swaraj something ---
        if self._detect_learning(text):
            if self.ai:
                response, lang = self.ai.think(text)
                facts = self.identity.data["memories"]["important_facts"]
                facts["latest_learning"] = text
                self.identity._save_data()
                return response, lang

        # --- Task Automation ---
        task_result = self.automation.execute_command(text, self.current_language)
        if task_result:
            return task_result, self.current_language

        # --- AI Brain ---
        if self.ai:
            response, lang = self.ai.think(text)
            return response, lang
        else:
            nickname = self.identity.get_random_nickname()
            return (f"Sorry {nickname}, I'm in basic mode. "
                    "I can open apps, search, tell time - but can't chat yet."), self.current_language

    def run_text_mode(self):
        owner_name = self.identity.get_owner_name() or "Shiva"
        if not self.identity.data["owner"]["is_trained"]:
            print("\nFirst time? Run: python swaraj.py --setup\n")

        greeting = {
            "english": f"Hey {owner_name}! Swaraj online. What's up?",
            "hindi": f"अरे {owner_name}! स्वराज ऑनलाइन। क्या हो रहा है?",
            "marathi": f"अरे {owner_name}! स्वराज ऑनलाइन. काय चाललं आहे?"
        }
        print(greeting.get(self.current_language, greeting["english"]))

        while True:
            try:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue

                response, lang = self.process_command(user_input)
                print(f"Swaraj: {response}")

                if "See you" in response:
                    break

            except KeyboardInterrupt:
                print(f"\nSwaraj: Later! I'll be here.")
                break

    def run_ui_mode(self):
        from ui import SwarajUI

        self.ui = SwarajUI()
        self.ui.on_send = self._ui_handle_input

        owner_name = self.identity.get_owner_name() or "Shiva"
        greeting = {
            "english": f"Hey {owner_name}! It's your best friend Swaraj.",
            "hindi": f"अरे {owner_name}! तुम्हारा best friend स्वराज।",
            "marathi": f"अरे {owner_name}! तुझा best friend स्वराज."
        }
        self.ui.set_response(greeting.get(self.current_language, greeting["english"]))
        self.ui.run()

    def _ui_handle_input(self, text):
        self.ui.set_state("thinking")
        self.ui.set_agent_status("THINKING")

        # Detect what kind of operation
        text_lower = text.lower()
        if "open" in text_lower:
            self.ui.set_agent_status("OPENING")
        elif "search" in text_lower:
            self.ui.set_agent_status("SEARCHING")
        elif "weather" in text_lower:
            self.ui.set_agent_status("FETCHING")

        response, lang = self.process_command(text)

        if "See you" in response or "bye" in response.lower():
            self.ui.set_response(response)
            self.ui.set_agent_status("OFFLINE")
            self.ui.root.after(1500, self.ui.destroy)
            return

        self.ui.set_state("speaking")
        self.ui.set_agent_status("SPEAKING")
        self.ui.set_response(response)

        # Return to idle after speaking
        self.ui.root.after(3000, lambda: self.ui.set_state("idle"))
        self.ui.root.after(3000, lambda: self.ui.set_agent_status("STANDBY"))

    def run_voice_mode(self, use_wake_word=True):
        owner_name = self.identity.get_owner_name() or "Shiva"
        greeting = {
            "english": f"Hey {owner_name}! Swaraj here. What do you need?",
            "hindi": f"अरे {owner_name}! स्वराज बोल रहा हूँ। बोलो।",
            "marathi": f"अरे {owner_name}! स्वराज बोलतोय. सांगा."
        }
        print(greeting.get(self.current_language, greeting["english"]))

        while True:
            try:
                if use_wake_word:
                    self.wake_detector.listen_for_wake_word()
                    print("Yes?")

                text = self.recognizer.listen(timeout=5, phrase_limit=10)
                if not text:
                    if not use_wake_word:
                        print("I didn't hear you. Try again.")
                    continue

                response, lang = self.process_command(text)
                print(f"Swaraj: {response}")

                if "See you" in response:
                    break

            except KeyboardInterrupt:
                print(f"\nSwaraj: Later!")
                break

    def run(self, mode="voice", use_wake_word=True):
        if mode == "setup":
            self.setup_mode()
        elif mode == "text":
            self.run_text_mode()
        elif mode == "ui":
            self.run_ui_mode()
        else:
            self.run_voice_mode(use_wake_word=use_wake_word)


def main():
    use_wake_word = True
    mode = "voice"
    language = "english"

    if "--text" in sys.argv:
        mode = "text"
    if "--ui" in sys.argv:
        mode = "ui"
    if "--setup" in sys.argv:
        mode = "setup"
    if "--voice" in sys.argv:
        mode = "voice"
        use_wake_word = False
    if "--no-wake" in sys.argv:
        use_wake_word = False
    if "--lang" in sys.argv:
        idx = sys.argv.index("--lang")
        if idx + 1 < len(sys.argv):
            language = sys.argv[idx + 1].lower()

    swaraj = Swaraj(use_ai=True, language=language)
    swaraj.run(mode=mode, use_wake_word=use_wake_word)


if __name__ == "__main__":
    main()
