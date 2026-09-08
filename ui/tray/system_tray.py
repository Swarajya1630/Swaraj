"""
System Tray Service
==================
Windows system tray icon for JARVIS.
Provides quick access and status indication.
"""

import os
import sys
import threading
from core.logger import logger

try:
    import pystray
    from pystray import MenuItem, Icon
    HAS_PYSTRAY = True
except ImportError:
    HAS_PYSTRAY = False
    logger.warning("pystray not installed. System tray unavailable.")


class SystemTray:
    def __init__(self):
        self.icon = None
        self._running = False
        self._callbacks = {
            "open": None,
            "pause": None,
            "resume": None,
            "settings": None,
            "restart": None,
            "status": None,
            "exit": None
        }
        self._status = "running"
        self._paused = False

    def set_callbacks(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._callbacks:
                self._callbacks[key] = value

    def _create_icon_image(self):
        """Create a simple icon for the tray."""
        try:
            from PIL import Image, ImageDraw

            img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            draw.ellipse([8, 8, 56, 56], fill=(0, 212, 255, 255), outline=(0, 100, 180, 255), width=2)
            draw.ellipse([20, 20, 44, 44], fill=(0, 50, 100, 255), outline=(0, 212, 255, 255), width=1)
            draw.ellipse([28, 28, 36, 36], fill=(255, 255, 255, 255))

            return img
        except ImportError:
            return None

    def start(self):
        if not HAS_PYSTRAY:
            logger.warning("System tray unavailable - pystray not installed")
            return False

        try:
            image = self._create_icon_image()

            menu = pystray.Menu(
                MenuItem("Open Assistant", lambda: self._trigger("open")),
                MenuItem("Pause Listening", lambda: self._trigger("pause")),
                MenuItem("Resume Listening", lambda: self._trigger("resume")),
                pystray.Menu.SEPARATOR,
                MenuItem("Settings", lambda: self._trigger("settings")),
                MenuItem("Restart", lambda: self._trigger("restart")),
                MenuItem("Status", lambda: self._trigger("status")),
                pystray.Menu.SEPARATOR,
                MenuItem("Exit", lambda: self._trigger("exit"))
            )

            self.icon = Icon(
                "SwarajAI",
                image,
                "Swaraj AI Assistant",
                menu
            )

            self._running = True
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
            logger.info("System tray started")
            return True

        except Exception as e:
            logger.error(f"System tray failed: {e}")
            return False

    def _run(self):
        try:
            self.icon.run()
        except Exception as e:
            logger.error(f"System tray error: {e}")

    def _trigger(self, action):
        callback = self._callbacks.get(action)
        if callback:
            try:
                callback()
            except Exception as e:
                logger.error(f"Tray callback error: {e}")

    def update_status(self, status):
        self._status = status
        if self.icon:
            status_text = {
                "running": "Swaraj - Listening",
                "paused": "Swaraj - Paused",
                "thinking": "Swaraj - Thinking",
                "speaking": "Swaraj - Speaking",
                "error": "Swaraj - Error"
            }
            self.icon.title = status_text.get(status, "Swaraj AI")

    def stop(self):
        if self.icon:
            self._running = False
            self.icon.stop()
            logger.info("System tray stopped")
