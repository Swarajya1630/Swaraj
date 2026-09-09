"""
Speech Recognition Module
========================
Converts your spoken words into text.
Supports offline (Vosk/Whisper) and online (Google) STT.
"""

import speech_recognition as sr
from core.logger import logger


class SpeechRecognizer:
    def __init__(self, language="en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        self._offline_stt = None
        self._use_offline = False

        self._init_offline_stt()

        self.languages = {
            "english": "en-US",
            "hindi": "hi-IN",
            "marathi": "mr-IN"
        }

    def _init_offline_stt(self):
        """Initialize offline STT if available."""
        try:
            from core.offline_stt import OfflineSTT
            self._offline_stt = OfflineSTT()
            if self._offline_stt.is_offline_available():
                self._use_offline = True
                logger.startup(f"Offline STT available: {self._offline_stt.get_available_backends()}")
            else:
                logger.info("Offline STT not available, using online only")
        except Exception as e:
            logger.info(f"Offline STT init skipped: {e}")

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
        """Listens to microphone and returns recognized text."""
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

        # Try offline STT first
        if self._use_offline and self._offline_stt:
            try:
                audio_data = audio.get_raw_data()
                text, lang = self._offline_stt.transcribe(audio_data=audio_data)
                if text:
                    print(f"You said: {text}")
                    return text
            except Exception as e:
                logger.warning(f"Offline STT failed: {e}")

        # Fallback to Google (online)
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            if self._use_offline and self._offline_stt:
                print("Offline STT also failed. Check audio input.")
            return None

    def is_offline_available(self):
        """Check if offline STT is available."""
        return self._use_offline and self._offline_stt and self._offline_stt.is_offline_available()
