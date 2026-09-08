"""
System Monitor Module
====================
Monitor CPU, RAM, disk, and battery status.
Provides system health info on demand.
"""

import psutil
import platform
from datetime import datetime


class SystemMonitor:
    def __init__(self):
        self.platform = platform.system()

    def get_cpu_usage(self):
        """Get CPU usage percentage."""
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        """Get RAM usage info."""
        mem = psutil.virtual_memory()
        return {
            "total": round(mem.total / (1024**3), 1),
            "used": round(mem.used / (1024**3), 1),
            "free": round(mem.available / (1024**3), 1),
            "percent": mem.percent
        }

    def get_disk_usage(self):
        """Get disk usage for C: drive."""
        disk = psutil.disk_usage('C:\\' if self.platform == 'Windows' else '/')
        return {
            "total": round(disk.total / (1024**3), 1),
            "used": round(disk.used / (1024**3), 1),
            "free": round(disk.free / (1024**3), 1),
            "percent": disk.percent
        }

    def get_battery_status(self):
        """Get battery status (laptop only)."""
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged": battery.power_plugged,
                "charging": battery.power_plugged and battery.percent < 100
            }
        return None

    def get_system_info(self):
        """Get full system status."""
        cpu = self.get_cpu_usage()
        mem = self.get_memory_usage()
        disk = self.get_disk_usage()
        battery = self.get_battery_status()

        info = {
            "cpu_percent": cpu,
            "ram": mem,
            "disk": disk,
            "battery": battery,
            "os": f"{platform.system()} {platform.release()}",
            "processor": platform.processor()
        }
        return info

    def get_status_text(self):
        """Get human-readable system status."""
        info = self.get_system_info()

        lines = ["System Status:"]
        lines.append(f"CPU: {info['cpu_percent']}%")
        lines.append(f"RAM: {info['ram']['used']}GB / {info['ram']['total']}GB ({info['ram']['percent']}%)")
        lines.append(f"Disk: {info['disk']['used']}GB / {info['disk']['total']}GB ({info['disk']['percent']}%)")

        if info['battery']:
            status = "Charging" if info['battery']['plugged'] else "On Battery"
            lines.append(f"Battery: {info['battery']['percent']}% ({status})")

        return "\n".join(lines)

    def get_health_report(self):
        """Get system health assessment."""
        info = self.get_system_info()
        issues = []

        if info['cpu_percent'] > 80:
            issues.append("High CPU usage")
        if info['ram']['percent'] > 80:
            issues.append("High RAM usage")
        if info['disk']['percent'] > 90:
            issues.append("Low disk space")

        if info['battery'] and not info['battery']['plugged'] and info['battery']['percent'] < 20:
            issues.append("Low battery!")

        if issues:
            return "⚠️ " + ", ".join(issues)
        return "✅ System running smoothly"


if __name__ == "__main__":
    monitor = SystemMonitor()
    print(monitor.get_status_text())
    print(monitor.get_health_report())
