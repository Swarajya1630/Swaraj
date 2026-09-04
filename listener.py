"""
Speech Recognition Module
=========================
Converts your spoken words into text using Google's Speech Recognition API.
Supports English, Hindi, and Marathi.
"""

import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self, language="en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        # Language mapping
        self.languages = {
            "english": "en-US",
            "hindi": "hi-IN",
            "marathi": "mr-IN"
        }

    def set_language(self, lang_name):
        """Switch recognition language."""
        lang_key = lang_name.lower().strip()
        if lang_key in self.languages:
            self.language = self.languages[lang_key]
            print(f"Language set to: {lang_name} ({self.language})")
            return True
        return False

    def detect_language_command(self, text):
        """Check if user wants to switch language."""
        text_lower = text.lower().strip()
        for lang_name in self.languages:
            if f"in {lang_name}" in text_lower or f"switch to {lang_name}" in text_lower:
                return lang_name
        return None

    def listen(self, timeout=5, phrase_limit=10):
        """
        Listens to microphone and returns recognized text.
        """
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
            except sr.WaitTimeoutError:
                return None

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            return None
