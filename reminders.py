"""
Reminders Module
================
Swaraj reminds you of tasks proactively.
Stores reminders and checks them periodically.
"""

import json
import os
from datetime import datetime, timedelta


class Reminders:
    def __init__(self, data_file="reminders.json"):
        self.data_file = os.path.join(os.path.dirname(__file__), data_file)
        self.reminders = self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.reminders, f, indent=2, ensure_ascii=False)

    def add(self, text, minutes=None, hours=None, days=None):
        """Add a reminder."""
        delay = timedelta()
        if minutes:
            delay += timedelta(minutes=minutes)
        if hours:
            delay += timedelta(hours=hours)
        if days:
            delay += timedelta(days=days)

        if delay == timedelta():
            delay = timedelta(minutes=5)  # Default 5 minutes

        remind_at = datetime.now() + delay

        reminder = {
            "id": len(self.reminders) + 1,
            "text": text,
            "created": datetime.now().isoformat(),
            "remind_at": remind_at.isoformat(),
            "done": False
        }
        self.reminders.append(reminder)
        self._save()
        return reminder

    def check(self):
        """Check for due reminders. Returns list of due reminders."""
        now = datetime.now()
        due = []
        for r in self.reminders:
            if not r["done"]:
                remind_time = datetime.fromisoformat(r["remind_at"])
                if now >= remind_time:
                    due.append(r)
                    r["done"] = True
        if due:
            self._save()
        return due

    def list_pending(self):
        """List all pending reminders."""
        return [r for r in self.reminders if not r["done"]]

    def remove(self, reminder_id):
        """Remove a reminder by ID."""
        self.reminders = [r for r in self.reminders if r["id"] != reminder_id]
        self._save()

    def clear_done(self):
        """Remove completed reminders."""
        self.reminders = [r for r in self.reminders if not r["done"]]
        self._save()


if __name__ == "__main__":
    r = Reminders()
    r.add("Drink water", minutes=30)
    r.add("Check emails", hours=1)
    print("Pending:", r.list_pending())
