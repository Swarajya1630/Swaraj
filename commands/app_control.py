"""
Application Control Commands
===========================
Open, close, and manage Windows applications.
Safe execution with allowlisted apps.
"""

import os
import subprocess
import webbrowser
from core.logger import logger


class AppControlCommand:
    DESKTOP_APPS = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "mozilla": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "terminal": "wt.exe",
        "powershell": "powershell.exe",
        "vscode": r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "visual studio code": r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "word": "winword.exe",
        "microsoft word": "winword.exe",
        "excel": "excel.exe",
        "microsoft excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "microsoft powerpoint": "powerpnt.exe",
        "paint": "mspaint.exe",
        "snipping tool": "SnippingTool.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
    }

    STORE_APPS = {
        "whatsapp": "whatsapp:",
        "spotify": "spotify:",
        "teams": "ms-teams:",
        "outlook": "outlook:",
        "photos": "ms-photos:",
        "maps": "bingmaps:",
        "settings": "ms-settings:",
        "store": "ms-windows-store:",
        "mail": "mailto:",
        "xbox": "xbox:",
    }

    SPECIAL_FOLDERS = {
        "downloads": os.path.expanduser("~\\Downloads"),
        "desktop": os.path.expanduser("~\\Desktop"),
        "documents": os.path.expanduser("~\\Documents"),
        "pictures": os.path.expanduser("~\\Pictures"),
        "music": os.path.expanduser("~\\Music"),
        "videos": os.path.expanduser("~\\Videos"),
        "my project": os.path.expanduser("~\\OneDrive\\Documents\\Default Project"),
        "project": os.path.expanduser("~\\OneDrive\\Documents\\Default Project"),
        "projects": os.path.expanduser("~\\OneDrive\\Documents\\Default Project"),
    }

    def __init__(self, app=None):
        self.app = app

    def execute(self, action, text):
        if action == "open":
            return self._open_app(text)
        elif action == "close":
            return self._close_app(text)
        elif action == "folder":
            return self._open_folder(text)
        return "Unknown app command.", "english"

    def _open_app(self, text):
        text_lower = text.lower()

        for name, path in self.DESKTOP_APPS.items():
            if name in text_lower:
                return self._launch_desktop_app(name, path)

        for name, uri in self.STORE_APPS.items():
            if name in text_lower:
                return self._launch_store_app(name, uri)

        app_name = text_lower
        for word in ["open", "launch", "start", "run", "भरा", "उघड", "करो", "कर"]:
            app_name = app_name.replace(word, "").strip()

        if app_name:
            try:
                subprocess.Popen(f"start {app_name}", shell=True)
                return f"Opening {app_name}.", "english"
            except Exception as e:
                logger.error(f"Failed to open {app_name}: {e}")
                return f"Couldn't open {app_name}.", "english"

        return "What would you like me to open?", "english"

    def _launch_desktop_app(self, name, path):
        path = path.replace("{user}", os.getlogin())
        try:
            if os.path.exists(path):
                subprocess.Popen(path)
                return f"Opening {name}.", "english"
            else:
                subprocess.Popen(f"start {name}", shell=True)
                return f"Trying to open {name}.", "english"
        except Exception as e:
            logger.error(f"Failed to open {name}: {e}")
            return f"Couldn't open {name}.", "english"

    def _launch_store_app(self, name, uri):
        try:
            os.system(f"start {uri}")
            return f"Opening {name}.", "english"
        except Exception as e:
            logger.error(f"Failed to open {name}: {e}")
            return f"Couldn't open {name}.", "english"

    def _close_app(self, text):
        text_lower = text.lower()
        app_name = text_lower
        for word in ["close", "quit", "exit", "band", "बंद", "करो", "बंद कर"]:
            app_name = app_name.replace(word, "").strip()

        process_map = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "notepad": "notepad.exe",
            "vscode": "Code.exe",
            "spotify": "Spotify.exe",
            "whatsapp": "WhatsApp.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
        }

        for name, process in process_map.items():
            if name in app_name:
                try:
                    os.system(f"taskkill /f /im {process}")
                    return f"Closing {name}.", "english"
                except Exception as e:
                    return f"Couldn't close {name}.", "english"

        return f"Which app should I close?", "english"

    def _open_folder(self, text):
        text_lower = text.lower()

        for name, path in self.SPECIAL_FOLDERS.items():
            if name in text_lower:
                try:
                    os.startfile(path)
                    return f"Opening {name} folder.", "english"
                except Exception as e:
                    return f"Couldn't open {name}.", "english"

        return "Which folder would you like to open?", "english"
