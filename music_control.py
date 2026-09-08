"""
Music Control Module
===================
Control music playback on Spotify or system media.
Supports play, pause, next, previous, volume.
"""

import subprocess
import os
import webbrowser


class MusicControl:
    def __init__(self):
        self.is_playing = False
        self.current_track = None

    def play_spotify(self, query=""):
        """Open and play on Spotify."""
        try:
            # Try opening Spotify URI
            if os.name == 'nt':  # Windows
                if query:
                    # Search on Spotify web
                    webbrowser.open(f"https://open.spotify.com/search/{query}")
                else:
                    # Open Spotify app
                    subprocess.Popen(["start", "spotify:"], shell=True)
            self.is_playing = True
            return f"Playing on Spotify" + (f": {query}" if query else "")
        except Exception as e:
            return f"Couldn't open Spotify: {str(e)}"

    def play_pause(self):
        """Toggle play/pause using media keys."""
        try:
            if os.name == 'nt':  # Windows
                # Send media play/pause key
                subprocess.run(["powershell", "-Command",
                    "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{MEDIA_PLAY_PAUSE}')"],
                    capture_output=True)
            self.is_playing = not self.is_playing
            return "Paused" if not self.is_playing else "Playing"
        except Exception as e:
            return f"Media control failed: {str(e)}"

    def next_track(self):
        """Skip to next track."""
        try:
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command",
                    "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{MEDIA_NEXT_TRACK}')"],
                    capture_output=True)
            return "Next track"
        except Exception as e:
            return f"Skip failed: {str(e)}"

    def previous_track(self):
        """Go to previous track."""
        try:
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command",
                    "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{MEDIA_PREV_TRACK}')"],
                    capture_output=True)
            return "Previous track"
        except Exception as e:
            return f"Previous failed: {str(e)}"

    def volume_up(self):
        """Increase system volume."""
        try:
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command",
                    "$wshShell = New-Object -ComObject WScript.Shell; 1..5 | ForEach-Object {$wshShell.SendKeys([char]175)}"],
                    capture_output=True)
            return "Volume up"
        except Exception as e:
            return f"Volume control failed: {str(e)}"

    def volume_down(self):
        """Decrease system volume."""
        try:
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command",
                    "$wshShell = New-Object -ComObject WScript.Shell; 1..5 | ForEach-Object {$wshShell.SendKeys([char]174)}"],
                    capture_output=True)
            return "Volume down"
        except Exception as e:
            return f"Volume control failed: {str(e)}"

    def mute(self):
        """Mute/unmute system volume."""
        try:
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command",
                    "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{VOLUME_MUTE}')"],
                    capture_output=True)
            return "Muted/Unmuted"
        except Exception as e:
            return f"Mute failed: {str(e)}"

    def play_youtube(self, query):
        """Play music on YouTube."""
        try:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}+music")
            return f"Playing {query} on YouTube"
        except Exception as e:
            return f"Couldn't open YouTube: {str(e)}"


if __name__ == "__main__":
    m = MusicControl()
    print(m.play_pause())
    print(m.next_track())
