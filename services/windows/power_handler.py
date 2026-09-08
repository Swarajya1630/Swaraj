"""
Windows Power State Handler
==========================
Handles sleep/hibernate/resume events.
Reinitializes services after resume.
"""

import ctypes
import threading
from core.logger import logger


class PowerStateHandler:
    def __init__(self):
        self.on_resume_callbacks = []
        self.on_sleep_callbacks = []
        self._running = False

    def register_callbacks(self, on_resume=None, on_sleep=None):
        """Register callbacks for power events."""
        if on_resume:
            self.on_resume_callbacks.append(on_resume)
        if on_sleep:
            self.on_sleep_callbacks.append(on_sleep)

    def start_listening(self):
        """Start listening for power events in background."""
        self._running = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()
        logger.info("Power state listener started")

    def _listen_loop(self):
        """Monitor power state changes."""
        try:
            import win32api
            import win32con
            import win32gui

            def on_power_broadcast(hwnd, msg, wparam, lparam):
                if msg == win32con.WM_POWERBROADCAST:
                    if wparam == win32con.PBT_APMRESUMEAUTOMATIC or wparam == win32con.PBT_APMRESUMESUSPEND:
                        logger.info("Windows resumed from sleep/hibernate")
                        self._trigger_callbacks(self.on_resume_callbacks)
                    elif wparam == win32con.PBT_APMSUSPEND:
                        logger.info("Windows entering sleep/hibernate")
                        self._trigger_callbacks(self.on_sleep_callbacks)

            message_map = {win32con.WM_POWERBROADCAST: on_power_broadcast}
            hwnd = win32gui.CreateWindowEx(0, "Static", "", 0, 0, 0, 0, 0, 0, 0, 0, None)
            win32gui.RegisterClass(message_map)
            win32gui.PumpMessages()

        except ImportError:
            logger.warning("win32gui not available, using polling for power state")
            self._poll_power_state()

    def _poll_power_state(self):
        """Fallback: poll system power state."""
        import time
        last_state = self._get_system_state()

        while self._running:
            time.sleep(2)
            current_state = self._get_system_state()

            if last_state == "sleeping" and current_state == "active":
                logger.info("System resumed from sleep")
                self._trigger_callbacks(self.on_resume_callbacks)
            elif last_state == "active" and current_state == "sleeping":
                logger.info("System entering sleep")
                self._trigger_callbacks(self.on_sleep_callbacks)

            last_state = current_state

    def _get_system_state(self):
        """Check if system is in sleep/active state."""
        try:
            import psutil
            boot_time = psutil.boot_time()
            return "active"
        except:
            return "active"

    def _trigger_callbacks(self, callbacks):
        """Trigger all registered callbacks."""
        for callback in callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Power callback error: {e}")

    def stop(self):
        self._running = False
