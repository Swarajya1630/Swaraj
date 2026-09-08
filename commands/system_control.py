"""
System Control Commands
======================
Time, date, system status, power operations.
"""

import datetime
import platform
from core.logger import logger


class SystemControlCommand:
    def __init__(self, app=None):
        self.app = app

    def execute(self, action, text):
        if action == "time":
            return self._get_time()
        elif action == "date":
            return self._get_date()
        elif action == "status":
            return self._get_status()
        elif action == "power":
            return self._power_action(text)
        elif action == "info":
            return self._get_info(text)
        return "Unknown system command.", "english"

    def _get_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"It's {time_str}.", "english"

    def _get_date(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}.", "english"

    def _get_status(self):
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('C:\\')

            status = f"System Status:\n"
            status += f"CPU: {cpu}%\n"
            status += f"RAM: {mem.percent}% ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)\n"
            status += f"Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"

            battery = psutil.sensors_battery()
            if battery:
                status += f"\nBattery: {battery.percent}%"
                if battery.power_plugged:
                    status += " (Charging)"

            return status, "english"
        except Exception as e:
            return f"System: {platform.system()} {platform.release()}", "english"

    def _power_action(self, text):
        text_lower = text.lower()

        if "shutdown" in text_lower or "shut down" in text_lower:
            logger.warning("Shutdown command received")
            return "I can't shut down your computer directly. Please use Windows shutdown.", "english"

        elif "restart" in text_lower:
            logger.warning("Restart command received")
            return "I can't restart your computer directly. Please use Windows restart.", "english"

        elif "sleep" in text_lower:
            logger.info("Sleep command received")
            try:
                import subprocess
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=False)
                return "Putting computer to sleep.", "english"
            except Exception as e:
                return "Couldn't put computer to sleep.", "english"

        elif "lock" in text_lower:
            logger.info("Lock command received")
            try:
                import subprocess
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
                return "Locking your computer.", "english"
            except Exception as e:
                return "Couldn't lock computer.", "english"

        return "What would you like me to do? (sleep, lock)", "english"

    def _get_info(self, text):
        text_lower = text.lower()

        if "time" in text_lower:
            return self._get_time()
        elif "date" in text_lower:
            return self._get_date()
        elif "status" in text_lower or "system" in text_lower:
            return self._get_status()
        elif "weather" in text_lower:
            return self._get_weather()

        return self._get_status()

    def _get_weather(self):
        try:
            import requests
            response = requests.get("https://wttr.in/?format=j1", timeout=10)
            data = response.json()
            current = data["current_condition"][0]
            temp = current["temp_C"]
            condition = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            return f"Weather: {temp}°C, {condition}. Humidity: {humidity}%.", "english"
        except Exception as e:
            return "Couldn't fetch weather right now.", "english"
