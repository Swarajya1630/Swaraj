"""
Windows Startup Service
======================
Registers JARVIS to start with Windows.
Uses Windows Registry for startup registration.
"""

import os
import sys
import winreg
from core.logger import logger


class StartupService:
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "SwarajAI"

    def __init__(self):
        self.app_path = os.path.abspath(sys.argv[0])
        self.python_path = sys.executable

    def is_enabled(self):
        """Check if startup is enabled."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REGISTRY_PATH, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, self.APP_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Startup check failed: {e}")
            return False

    def enable(self):
        """Enable startup with Windows."""
        try:
            if self.app_path.endswith(".py"):
                cmd = f'"{self.python_path}" "{self.app_path}" --startup'
            elif self.app_path.endswith(".pyw"):
                pythonw = os.path.join(os.path.dirname(self.python_path), "pythonw.exe")
                if os.path.exists(pythonw):
                    cmd = f'"{pythonw}" "{self.app_path}" --startup'
                else:
                    cmd = f'"{self.python_path}" "{self.app_path}" --startup'
            else:
                cmd = f'"{self.app_path}" --startup'

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, self.APP_NAME, 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(key)
            logger.startup("Startup enabled")
            return True
        except Exception as e:
            logger.error(f"Failed to enable startup: {e}")
            return False

    def disable(self):
        """Disable startup with Windows."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, self.APP_NAME)
            winreg.CloseKey(key)
            logger.startup("Startup disabled")
            return True
        except FileNotFoundError:
            return True
        except Exception as e:
            logger.error(f"Failed to disable startup: {e}")
            return False
