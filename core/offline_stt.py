"""
Offline Speech-to-Text
=====================
Works without internet using Vosk or Whisper.
Falls back to Google API when online.
"""

import os
import json
import wave
import tempfile
from core.logger import logger


class OfflineSTT:
    def __init__(self):
        self._vosk_model = None
        self._whisper_model = None
        self._recognizer = None
        self._available_backends = []

        self._init_backends()

    def _init_backends(self):
        """Initialize available STT backends."""

        # Try Vosk (offline)
        try:
            from vosk import Model, KaldiRecognizer
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "vosk_model")
            if os.path.exists(model_path):
                self._vosk_model = Model(model_path)
                self._available_backends.append("vosk")
                logger.startup("Vosk STT initialized")
            else:
                logger.info("Vosk model not found, downloading small model...")
                self._try_download_vosk()
        except ImportError:
            logger.info("Vosk not installed")
        except Exception as e:
            logger.warning(f"Vosk init failed: {e}")

        # Try Whisper (offline)
        try:
            import whisper
            self._whisper_model = whisper.load_model("base")
            self._available_backends.append("whisper")
            logger.startup("Whisper STT initialized")
        except ImportError:
            logger.info("Whisper not installed")
        except Exception as e:
            logger.warning(f"Whisper init failed: {e}")

        # Try SpeechRecognition (online fallback)
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._available_backends.append("google")
            logger.startup("Google STT available (online)")
        except ImportError:
            logger.warning("SpeechRecognition not installed")

        if not self._available_backends:
            logger.warning("No STT backend available!")

    def _try_download_vosk(self):
        """Try to download Vosk small model."""
        try:
            import urllib.request
            import zipfile

            model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
            model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "vosk_model")

            logger.info("Downloading Vosk model (50MB)...")
            zip_path = os.path.join(model_dir, "model.zip")

            os.makedirs(model_dir, exist_ok=True)
            urllib.request.urlretrieve(model_url, zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(model_dir)

            os.remove(zip_path)

            # Find the extracted folder
            for item in os.listdir(model_dir):
                item_path = os.path.join(model_dir, item)
                if os.path.isdir(item_path) and "vosk" in item.lower():
                    # Move contents up
                    for sub_item in os.listdir(item_path):
                        src = os.path.join(item_path, sub_item)
                        dst = os.path.join(model_dir, sub_item)
                        os.rename(src, dst)
                    os.rmdir(item_path)
                    break

            from vosk import Model
            self._vosk_model = Model(model_dir)
            self._available_backends.append("vosk")
            logger.startup("Vosk model downloaded and initialized")

        except Exception as e:
            logger.warning(f"Vosk download failed: {e}")

    def transcribe(self, audio_data=None, audio_file=None):
        """Transcribe audio using available backend."""

        # Try Vosk first (offline)
        if "vosk" in self._available_backends and self._vosk_model:
            return self._transcribe_vosk(audio_data, audio_file)

        # Try Whisper (offline)
        if "whisper" in self._available_backends and self._whisper_model:
            return self._transcribe_whisper(audio_data, audio_file)

        # Fallback to Google (online)
        if "google" in self._available_backends and self._recognizer:
            return self._transcribe_google(audio_data, audio_file)

        return None, "No STT backend available"

    def _transcribe_vosk(self, audio_data=None, audio_file=None):
        """Transcribe using Vosk (offline)."""
        try:
            from vosk import KaldiRecognizer

            if audio_file:
                wf = wave.open(audio_file, "rb")
            elif audio_data:
                tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                tmp.write(audio_data)
                tmp.close()
                wf = wave.open(tmp.name, "rb")
                os.unlink(tmp.name)
            else:
                return None, "No audio provided"

            rec = KaldiRecognizer(self._vosk_model, wf.getframerate())
            rec.SetWords(True)

            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get("text"):
                        results.append(result["text"])

            final = json.loads(rec.FinalResult())
            if final.get("text"):
                results.append(final["text"])

            wf.close()

            text = " ".join(results).strip()
            if text:
                return text, "english"
            return None, "No speech detected"

        except Exception as e:
            logger.error(f"Vosk STT failed: {e}")
            return None, f"Vosk error: {str(e)}"

    def _transcribe_whisper(self, audio_data=None, audio_file=None):
        """Transcribe using Whisper (offline)."""
        try:
            import numpy as np

            if audio_file:
                result = self._whisper_model.transcribe(audio_file)
            elif audio_data:
                tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                tmp.write(audio_data)
                tmp.close()
                result = self._whisper_model.transcribe(tmp.name)
                os.unlink(tmp.name)
            else:
                return None, "No audio provided"

            text = result.get("text", "").strip()
            if text:
                lang = result.get("language", "en")
                return text, lang
            return None, "No speech detected"

        except Exception as e:
            logger.error(f"Whisper STT failed: {e}")
            return None, f"Whisper error: {str(e)}"

    def _transcribe_google(self, audio_data=None, audio_file=None):
        """Transcribe using Google API (online fallback)."""
        try:
            import speech_recognition as sr

            if audio_file:
                with sr.AudioFile(audio_file) as source:
                    audio = self._recognizer.record(source)
            elif audio_data:
                tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                tmp.write(audio_data)
                tmp.close()
                with sr.AudioFile(tmp.name) as source:
                    audio = self._recognizer.record(source)
                os.unlink(tmp.name)
            else:
                return None, "No audio provided"

            text = self._recognizer.recognize_google(audio)
            return text, "english"

        except sr.UnknownValueError:
            return None, "Could not understand audio"
        except sr.RequestError as e:
            return None, f"Google STT error: {str(e)}"
        except Exception as e:
            return None, f"STT error: {str(e)}"

    def get_available_backends(self):
        """List available STT backends."""
        return self._available_backends

    def is_offline_available(self):
        """Check if offline STT is available."""
        return "vosk" in self._available_backends or "whisper" in self._available_backends
