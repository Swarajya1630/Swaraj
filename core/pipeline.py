"""
Speech Pipeline
==============
Integrates wake word → listen → process → respond cycle.
Handles the complete voice interaction flow.
Works offline with Vosk/Whisper STT.
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
        self._offline_stt = None

    def initialize(self):
        try:
            from core.wake_word_local import LocalWakeWordDetector
            self.wake_detector = LocalWakeWordDetector()
            self.wake_detector.set_callback(self._on_wake_word)

            self._init_offline_stt()

            logger.info("Speech pipeline initialized")
            return True
        except Exception as e:
            logger.error(f"Speech pipeline init failed: {e}")
            return False

    def _init_offline_stt(self):
        """Initialize offline STT for command recognition."""
        try:
            from core.offline_stt import OfflineSTT
            self._offline_stt = OfflineSTT()
            if self._offline_stt.is_offline_available():
                logger.startup(f"Pipeline offline STT: {self._offline_stt.get_available_backends()}")
        except Exception as e:
            logger.info(f"Pipeline offline STT not available: {e}")

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

        if self.app and self.app.sound:
            self.app.sound.play_wake()

        if self.app and self.app.ui_compact:
            self.app.ui_compact.set_state("listening")
            self.app.ui_compact.set_status("LISTENING")

        if self.app and self.app.tray:
            self.app.tray.update_status("listening")

        # Ask for command after wake
        self._ask_for_command()

    def _ask_for_command(self):
        """Prompt user for command after wake word."""
        if self.app and self.app.sound:
            try:
                self.app.sound.play("listening")
            except:
                pass

        # Speak prompt
        prompt = "Hello Shiva. What would you like me to do? I can open apps like OpenCode, YouTube, Canva, Opera GX, or listen to your command."

        if self.app and self.app.sound:
            try:
                self.app.sound.speak(prompt)
            except:
                pass

        logger.info(f"Prompt user: {prompt}")

    def _listen_for_command(self):

    def _listen_for_command(self):
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = None

            # Try offline STT first
            if self._offline_stt and self._offline_stt.is_offline_available():
                try:
                    audio_data = audio.get_raw_data()
                    text, lang = self._offline_stt.transcribe(audio_data=audio_data)
                    if text:
                        logger.info(f"Command heard (offline): {text}")
                except Exception as e:
                    logger.debug(f"Offline STT failed: {e}")

            # Fallback to Google (online)
            if not text:
                for lang in ["en-US", "hi-IN", "mr-IN"]:
                    try:
                        text = recognizer.recognize_google(audio, language=lang)
                        break
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        logger.warning("Google STT unavailable")
                        break

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

    def listen_and_respond(self):
        """Listen for a single command and respond (used by wake-after-sleep)."""
        self._on_wake_word()
