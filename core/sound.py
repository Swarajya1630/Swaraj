"""
Sound Feedback System
====================
Audio cues for Swaraj states (wake, listen, think, speak, error).
Generates tones programmatically - no external audio files needed.
"""

import threading
import math
import struct
import io
from core.logger import logger

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False


class SoundFeedback:
    def __init__(self):
        self.enabled = True
        self.volume = 0.3
        self._queue = []
        self._playing = False

    def _generate_tone(self, frequency, duration, volume=0.3, sample_rate=44100):
        """Generate a sine wave tone."""
        num_samples = int(sample_rate * duration)
        max_amplitude = 32767 * volume

        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            envelope = 1.0
            if t < 0.01:
                envelope = t / 0.01
            elif t > duration - 0.01:
                envelope = (duration - t) / 0.01

            value = int(max_amplitude * envelope * math.sin(2 * math.pi * frequency * t))
            samples.append(struct.pack('h', max(-32768, min(32767, value))))

        return b''.join(samples)

    def _play_bytes(self, audio_bytes, sample_rate=44100):
        """Play raw audio bytes."""
        if not HAS_PYAUDIO or not self.enabled:
            return

        try:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                output=True
            )
            stream.write(audio_bytes)
            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception as e:
            logger.debug(f"Sound playback error: {e}")

    def play_tone(self, frequency, duration):
        """Play a tone in a thread."""
        if not self.enabled:
            return

        def _play():
            audio = self._generate_tone(frequency, duration, self.volume)
            self._play_bytes(audio)

        threading.Thread(target=_play, daemon=True).start()

    def play_wake(self):
        """Play wake-up sound (ascending chime)."""
        def _play():
            self.play_tone(523, 0.08)
            import time; time.sleep(0.08)
            self.play_tone(659, 0.08)
            import time; time.sleep(0.08)
            self.play_tone(784, 0.12)
        threading.Thread(target=_play, daemon=True).start()

    def play_listening(self):
        """Play listening start sound."""
        self.play_tone(880, 0.05)

    def play_thinking(self):
        """Play thinking sound."""
        self.play_tone(440, 0.1)

    def play_success(self):
        """Play success sound (two ascending tones)."""
        def _play():
            self.play_tone(523, 0.08)
            import time; time.sleep(0.08)
            self.play_tone(784, 0.1)
        threading.Thread(target=_play, daemon=True).start()

    def play_error(self):
        """Play error sound (descending tones)."""
        def _play():
            self.play_tone(440, 0.1)
            import time; time.sleep(0.1)
            self.play_tone(330, 0.15)
        threading.Thread(target=_play, daemon=True).start()

    def play_notification(self):
        """Play notification sound."""
        self.play_tone(660, 0.06)

    def play_click(self):
        """Play UI click sound."""
        self.play_tone(1000, 0.02)

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
