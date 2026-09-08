"""
Speech Pipeline
==============
Integrates wake word → listen → process → respond cycle.
Handles the complete voice interaction flow.
"""

import threading
import time
from core.logger import logger


class SpeechPipeline:
    def __init__(self, app=None):
        self.app = app
        self._running = False
        self._active = False
        self._thread = None

        self.wake_detector = None
        self.recognizer = None
        self.speaker = None

    def initialize(self):
        try:
            from core.wake_word_local import LocalWakeWordDetector
            self.wake_detector = LocalWakeWordDetector()
            self.wake_detector.set_callback(self._on_wake_word)
            logger.info("Speech pipeline initialized")
            return True
        except Exception as e:
            logger.error(f"Speech pipeline init failed: {e}")
            return False

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._pipeline_loop, daemon=True)
        self._thread.start()
        logger.info("Speech pipeline started")

    def stop(self):
        self._running = False
        if self.wake_detector:
            self.wake_detector.stop()
        logger.info("Speech pipeline stopped")

    def _pipeline_loop(self):
        if self.wake_detector:
            self.wake_detector.start()

        while self._running:
            time.sleep(0.1)

    def _on_wake_word(self):
        logger.info("Wake word detected - entering active listening")
        self._active = True

        if self.app and self.app.ui_compact:
            self.app.ui_compact.set_state("listening")
            self.app.ui_compact.set_status("LISTENING")

        if self.app and self.app.tray:
            self.app.tray.update_status("listening")

        self._listen_for_command()

    def _listen_for_command(self):
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = None
            for lang in ["en-US", "hi-IN", "mr-IN"]:
                try:
                    text = recognizer.recognize_google(audio, language=lang)
                    break
                except sr.UnknownValueError:
                    continue

            if text:
                logger.info(f"Command heard: {text}")
                self._process_command(text)
            else:
                logger.debug("No command recognized")

        except sr.WaitTimeoutError:
            logger.debug("Listening timeout")
        except Exception as e:
            logger.error(f"Listen error: {e}")

        self._active = False
        if self.app and self.app.ui_compact:
            self.app.ui_compact.set_state("idle")
            self.app.ui_compact.set_status("STANDBY")

        if self.app and self.app.tray:
            self.app.tray.update_status("running")

    def _process_command(self, text):
        if self.app and self.app.ui_compact:
            self.app.ui_compact.set_state("thinking")
            self.app.ui_compact.set_status("THINKING")

        if self.app:
            response, lang = self.app._process_command(text)

            if self.app.ui_compact:
                self.app.ui_compact.set_state("speaking")
                self.app.ui_compact.set_status("SPEAKING")

                if self.app.ui_compact.expanded_window:
                    self.app.ui_compact.expanded_window.add_message("You", text)
                    self.app.ui_compact.expanded_window.add_message("Swaraj", response)

            self._speak(response, lang)

    def _speak(self, text, language="english"):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.setProperty('volume', 0.9)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")

    def is_active(self):
        return self._active
