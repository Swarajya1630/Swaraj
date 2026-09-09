"""
Local Wake Word Detector
========================
Detects wake words locally without cloud API.
Uses energy-based detection + local STT.
"""

import threading
import time
import struct
import queue
from core.logger import logger

try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    HAS_SR = False

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False


class LocalWakeWordDetector:
    def __init__(self, wake_words=None, energy_threshold=3000):
        self.wake_words = wake_words or ["hey swaraj", "swaraj"]
        self.energy_threshold = energy_threshold
        self._running = False
        self._listening = False
        self._callback = None
        self._thread = None
        self._offline_stt = None

        if HAS_SR:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = energy_threshold
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8

        self._init_offline_stt()

    def _init_offline_stt(self):
        """Initialize offline STT for wake word detection."""
        try:
            from core.offline_stt import OfflineSTT
            self._offline_stt = OfflineSTT()
            if self._offline_stt.is_offline_available():
                logger.startup("Offline wake word STT available")
        except Exception as e:
            logger.info(f"Offline wake word STT not available: {e}")

    def set_callback(self, callback):
        self._callback = callback

    def start(self):
        if self._running:
            return
        self._running = True
        self._listening = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        logger.info("Wake word detector started")

    def stop(self):
        self._running = False
        self._listening = False
        logger.info("Wake word detector stopped")

    def pause(self):
        self._listening = False

    def resume(self):
        self._listening = True

    def _listen_loop(self):
        if not HAS_SR:
            logger.error("SpeechRecognition not available")
            return

        mic = sr.Microphone()
        with mic as source:
            logger.info("Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone calibrated")

            while self._running:
                if not self._listening:
                    time.sleep(0.1)
                    continue

                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    self._process_audio(audio)
                except sr.WaitTimeoutError:
                    continue
                except OSError as e:
                    logger.error(f"Microphone error: {e}")
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Wake word error: {e}")
                    time.sleep(1)

    def _process_audio(self, audio):
        # Try offline STT first
        if self._offline_stt and self._offline_stt.is_offline_available():
            try:
                audio_data = audio.get_raw_data()
                text, lang = self._offline_stt.transcribe(audio_data=audio_data)
                if text:
                    text = text.lower()
                    logger.debug(f"Wake word heard (offline): '{text}'")
                    for phrase in self.wake_words:
                        if phrase in text:
                            logger.info(f"Wake word detected: {phrase}")
                            if self._callback:
                                self._callback()
                            return
            except Exception as e:
                logger.debug(f"Offline wake word STT failed: {e}")

        # Fallback to Google (online)
        for lang in ["en-US", "hi-IN", "mr-IN"]:
            try:
                text = self.recognizer.recognize_google(audio, language=lang).lower()
                logger.debug(f"Wake word heard: '{text}' ({lang})")

                for phrase in self.wake_words:
                    if phrase in text:
                        logger.info(f"Wake word detected: {phrase}")
                        if self._callback:
                            self._callback()
                        return

            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                logger.warning("Google STT unavailable, using offline only")
                break
            except Exception as e:
                logger.debug(f"Wake word STT error ({lang}): {e}")
                continue


class EnergyBasedWakeDetector:
    def __init__(self, threshold=500, callback=None):
        self.threshold = threshold
        self._callback = callback
        self._running = False

    def set_callback(self, callback):
        self._callback = callback

    def start(self):
        if not HAS_PYAUDIO:
            logger.error("PyAudio not available for energy detection")
            return

        self._running = True
        thread = threading.Thread(target=self._detect_loop, daemon=True)
        thread.start()
        logger.info("Energy-based wake detector started")

    def stop(self):
        self._running = False

    def _detect_loop(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )

        while self._running:
            try:
                data = stream.read(1024, exception_on_overflow=False)
                volume = self._get_volume(data)

                if volume > self.threshold:
                    logger.info(f"Energy spike detected: {volume}")
                    if self._callback:
                        self._callback()

                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Energy detection error: {e}")
                time.sleep(1)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def _get_volume(self, data):
        """Calculate volume from audio data."""
        count = len(data) / 2
        shorts = struct.unpack(f"{int(count)}h", data)
        sum_squares = sum(s ** 2 for s in shorts)
        return (sum_squares / count) ** 0.5
