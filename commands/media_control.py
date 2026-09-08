"""
Media Control Commands
=====================
Volume, playback, music control.
"""

import os
import subprocess
import webbrowser
from core.logger import logger


class MediaControlCommand:
    def __init__(self, app=None):
        self.app = app

    def execute(self, action, text):
        if action == "volume":
            return self._volume_control(text)
        elif action == "playback":
            return self._playback_control(text)
        elif action == "play":
            return self._play_music(text)
        return "Unknown media command.", "english"

    def _volume_control(self, text):
        text_lower = text.lower()

        if "up" in text_lower or "बढ़ाओ" in text_lower or "increase" in text_lower:
            return self._volume_up()
        elif "down" in text_lower or "कम" in text_lower or "decrease" in text_lower:
            return self._volume_down()
        elif "mute" in text_lower or "चुप" in text_lower:
            return self._mute()
        elif "unmute" in text_lower:
            return self._unmute()

        return "Volume up, down, or mute?", "english"

    def _volume_up(self):
        try:
            for _ in range(5):
                subprocess.run(["powershell", "-Command",
                    "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]175)"],
                    capture_output=True)
            return "Volume up.", "english"
        except Exception as e:
            return "Couldn't adjust volume.", "english"

    def _volume_down(self):
        try:
            for _ in range(5):
                subprocess.run(["powershell", "-Command",
                    "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]174)"],
                    capture_output=True)
            return "Volume down.", "english"
        except Exception as e:
            return "Couldn't adjust volume.", "english"

    def _mute(self):
        try:
            subprocess.run(["powershell", "-Command",
                "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{VOLUME_MUTE}')"],
                capture_output=True)
            return "Muted.", "english"
        except Exception as e:
            return "Couldn't mute.", "english"

    def _unmute(self):
        return self._mute()

    def _playback_control(self, text):
        text_lower = text.lower()

        if "play" in text_lower or "resume" in text_lower:
            return self._media_key("play")
        elif "pause" in text_lower:
            return self._media_key("pause")
        elif "stop" in text_lower:
            return self._media_key("stop")
        elif "next" in text_lower:
            return self._media_key("next")
        elif "previous" in text_lower or "back" in text_lower:
            return self._media_key("previous")

        return "Play, pause, stop, next, or previous?", "english"

    def _media_key(self, action):
        key_map = {
            "play": "{MEDIA_PLAY_PAUSE}",
            "pause": "{MEDIA_PLAY_PAUSE}",
            "stop": "{MEDIA_STOP}",
            "next": "{MEDIA_NEXT_TRACK}",
            "previous": "{MEDIA_PREV_TRACK}"
        }

        key = key_map.get(action)
        if not key:
            return "Unknown media action.", "english"

        try:
            subprocess.run(["powershell", "-Command",
                f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{key}')"],
                capture_output=True)
            return f"{action.capitalize()}.", "english"
        except Exception as e:
            return f"Couldn't {action}.", "english"

    def _play_music(self, text):
        text_lower = text.lower()

        if "spotify" in text_lower:
            query = text_lower
            for word in ["play", "चालवा", "on", "spotify", "music", "गाना", "म्यूजिक"]:
                query = query.replace(word, "").strip()
            try:
                if query:
                    webbrowser.open(f"https://open.spotify.com/search/{query}")
                    return f"Playing {query} on Spotify.", "english"
                else:
                    os.system("start spotify:")
                    return "Opening Spotify.", "english"
            except Exception as e:
                return "Couldn't open Spotify.", "english"

        elif "youtube" in text_lower:
            query = text_lower
            for word in ["play", "चालवा", "on", "youtube", "music", "गाना", "म्यूजिक"]:
                query = query.replace(word, "").strip()
            try:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}+music")
                return f"Playing {query} on YouTube.", "english"
            except Exception as e:
                return "Couldn't open YouTube.", "english"

        return "Play on Spotify or YouTube?", "english"
