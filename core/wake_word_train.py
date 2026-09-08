"""
Custom Wake Word Training
========================
Record and train custom wake words.
Uses audio recording and pattern matching.
"""

import os
import json
import wave
import struct
from datetime import datetime
from core.logger import logger

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False


class WakeWordTrainer:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "wake_words")
        os.makedirs(self.data_dir, exist_ok=True)

        self.custom_words_file = os.path.join(self.data_dir, "custom_words.json")
        self.custom_words = self._load()
        self.recordings_dir = os.path.join(self.data_dir, "recordings")
        os.makedirs(self.recordings_dir, exist_ok=True)

    def _load(self):
        if os.path.exists(self.custom_words_file):
            try:
                with open(self.custom_words_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"words": [], "settings": {"record_duration": 3, "sample_rate": 16000}}

    def _save(self):
        with open(self.custom_words_file, "w", encoding="utf-8") as f:
            json.dump(self.custom_words, f, indent=2, ensure_ascii=False)

    def is_available(self):
        return HAS_PYAUDIO

    def record_sample(self, phrase, duration=3):
        """Record a sample of the wake word."""
        if not HAS_PYAUDIO:
            return None, "PyAudio not installed"

        try:
            sample_rate = self.custom_words["settings"]["sample_rate"]
            chunk = 1024
            format = pyaudio.paInt16
            channels = 1

            p = pyaudio.PyAudio()
            stream = p.open(format=format, channels=channels, rate=sample_rate,
                          input=True, frames_per_buffer=chunk)

            frames = []
            for _ in range(0, int(sample_rate / chunk * duration)):
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{phrase.replace(' ', '_')}_{timestamp}.wav"
            filepath = os.path.join(self.recordings_dir, filename)

            wf = wave.open(filepath, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()

            return filepath, f"Recorded: {filename}"

        except Exception as e:
            logger.error(f"Recording failed: {e}")
            return None, f"Recording failed: {str(e)}"

    def add_wake_word(self, phrase, text_representation=None):
        """Add a custom wake word."""
        phrase = phrase.lower().strip()

        for word in self.custom_words["words"]:
            if word["phrase"] == phrase:
                return None, f"Wake word '{phrase}' already exists"

        word_entry = {
            "id": len(self.custom_words["words"]) + 1,
            "phrase": phrase,
            "text_representation": text_representation or phrase,
            "samples": [],
            "created": datetime.now().isoformat(),
            "enabled": True
        }

        self.custom_words["words"].append(word_entry)
        self._save()

        return word_entry["id"], f"Wake word '{phrase}' added"

    def remove_wake_word(self, phrase):
        """Remove a custom wake word."""
        phrase = phrase.lower().strip()
        self.custom_words["words"] = [w for w in self.custom_words["words"] if w["phrase"] != phrase]
        self._save()

    def enable_wake_word(self, phrase, enabled=True):
        """Enable or disable a wake word."""
        phrase = phrase.lower().strip()
        for word in self.custom_words["words"]:
            if word["phrase"] == phrase:
                word["enabled"] = enabled
                self._save()
                return True
        return False

    def list_wake_words(self):
        """List all custom wake words."""
        return self.custom_words["words"]

    def check_wake_word(self, text):
        """Check if text contains any custom wake word."""
        text_lower = text.lower()
        for word in self.custom_words["words"]:
            if word["enabled"] and word["phrase"] in text_lower:
                return True
        return False

    def get_wake_phrases(self):
        """Get all enabled wake phrases."""
        return [w["phrase"] for w in self.custom_words["words"] if w["enabled"]]
