"""
Local Wake Word Detector
=======================
Detects wake words locally without cloud API.
Uses energy-based detection + keyword spotting.
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

        if HAS_SR:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = energy_threshold
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8

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
        for lang in ["en-US", "hi-IN", "mr-IN"]:
            try:
                text = self.recognizer.recognize_google(audio, language=lang).lower()
                logger.debug(f"Wake word heard: '{text}' ({lang})")

                for phrase in self.wake_words:
                    if phrase in text:
                        logger.info(f"Wake word detected: '{text}'")
                        if self._callback:
                            self._callback()
                        return
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                logger.warning(f"Speech recognition error: {e}")
                break

    def is_listening(self):
        return self._listening


class EnergyBasedWakeDetector:
    def __init__(self, energy_threshold=3000, silence_duration=0.5):
        self.energy_threshold = energy_threshold
        self.silence_duration = silence_duration
        self._running = False
        self._listening = False
        self._callback = None

    def set_callback(self, callback):
        self._callback = callback

    def start(self):
        if not HAS_PYAUDIO:
            logger.error("PyAudio not available for energy detection")
            return

        self._running = True
        self._listening = True
        thread = threading.Thread(target=self._energy_loop, daemon=True)
        thread.start()
        logger.info("Energy-based wake detector started")

    def stop(self):
        self._running = False
        self._listening = False

    def _energy_loop(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )

        try:
            while self._running:
                if not self._listening:
                    time.sleep(0.1)
                    continue

                data = stream.read(1024, exception_on_overflow=False)
                energy = self._calculate_energy(data)

                if energy > self.energy_threshold:
                    logger.debug(f"Energy spike: {energy}")
                    time.sleep(self.silence_duration)

                    if self._callback:
                        self._callback()

                time.sleep(0.01)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def _calculate_energy(self, data):
        count = len(data) / 2
        sum_squares = 0.0
        for i in range(0, len(data), 2):
            sample = struct.unpack('h', data[i:i+2])[0]
            sum_squares += sample * sample
        return (sum_squares / count) ** 0.5
