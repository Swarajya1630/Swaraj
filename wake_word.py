"""
Wake Word Detection Module
==========================
Detects when you say "Hey Swaraj" (or Hindi/Marathi equivalents) to activate.
Supports: English, Hindi, Marathi wake words.
"""

import speech_recognition as sr


class WakeWordDetector:
    def __init__(self, wake_phrases=None):
        self.recognizer = sr.Recognizer()
        self.wake_phrases = wake_phrases or [
            # English
            "hey swaraj", "hello swaraj", "swaraj", "ok swaraj", "hi swaraj",
            # Hindi
            "अरे स्वराज", "स्वराज", "हेलो स्वराज", "ओके स्वराज",
            # Marathi
            "अरे स्वराज", "स्वराज", "हॅलो स्वराज", "ओके स्वराज",
        ]
        # Remove duplicates
        self.wake_phrases = list(dict.fromkeys(self.wake_phrases))
        self.is_listening = False

    def listen_for_wake_word(self, timeout=None):
        """
        Continuously listen until wake word is detected.
        Listens in all three languages.
        """
        with sr.Microphone() as source:
            print("Say 'Hey Swaraj' / 'अरे स्वराज' / 'हॅलो स्वराज' to activate...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)

                    # Try recognizing in all three languages
                    for lang in ["en-US", "hi-IN", "mr-IN"]:
                        try:
                            text = self.recognizer.recognize_google(audio, language=lang).lower()

                            for phrase in self.wake_phrases:
                                if phrase in text:
                                    print(f"Activated! (heard: '{text}' in {lang})")
                                    return True
                        except sr.UnknownValueError:
                            continue

                except sr.WaitTimeoutError:
                    continue
                except KeyboardInterrupt:
                    return False
