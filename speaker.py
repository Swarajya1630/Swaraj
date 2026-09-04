"""
Text-to-Speech Module
=====================
Converts text into spoken voice output using pyttsx3.
Supports English, Hindi, and Marathi voices.
"""

import pyttsx3


class Speaker:
    def __init__(self, rate=175, volume=0.9, voice_index=0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

        self.voices = self.engine.getProperty('voices')
        if self.voices and voice_index < len(self.voices):
            self.engine.setProperty('voice', self.voices[voice_index].id)

        # Build language -> voice index mapping
        self.voice_map = self._build_voice_map()

    def _build_voice_map(self):
        """Map languages to available voice indices."""
        voice_map = {"en": [], "hi": [], "mr": []}
        for i, voice in enumerate(self.voices):
            voice_id = voice.id.lower()
            voice_name = voice.name.lower()
            langs = [str(l).lower() for l in voice.languages] if voice.languages else []

            if "en" in voice_id or "english" in voice_name or any("en" in l for l in langs):
                voice_map["en"].append(i)
            elif "hi" in voice_id or "hindi" in voice_name or any("hi" in l for l in langs):
                voice_map["hi"].append(i)
            elif "mr" in voice_id or "marathi" in voice_name or any("mr" in l for l in langs):
                voice_map["mr"].append(i)

        # If no specific voices found, all voices work for English
        if not voice_map["en"]:
            voice_map["en"] = list(range(len(self.voices)))

        return voice_map

    def speak(self, text, language="en"):
        """Speak the given text out loud in the specified language."""
        print(f"Swaraj ({language}): {text}")

        # Try to switch to language-specific voice
        if language in self.voice_map and self.voice_map[language]:
            idx = self.voice_map[language][0]
            if idx < len(self.voices):
                self.engine.setProperty('voice', self.voices[idx].id)

        self.engine.say(text)
        self.engine.runAndWait()

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))

    def list_voices(self):
        """Print all available voices."""
        for i, voice in enumerate(self.voices):
            print(f"Voice {i}: {voice.name} ({voice.languages})")
