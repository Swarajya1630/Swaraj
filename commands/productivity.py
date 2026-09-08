"""
Productivity Commands
====================
Reminders, notes, and productivity features.
"""

import re
import json
import os
from datetime import datetime, timedelta
from core.logger import logger


class ProductivityCommand:
    def __init__(self, app=None):
        self.app = app
        self.notes_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "notes.json")
        self.reminders = []
        self.notes = self._load_notes()

    def _load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_notes(self):
        os.makedirs(os.path.dirname(self.notes_file), exist_ok=True)
        with open(self.notes_file, "w") as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)

    def execute(self, action, text):
        if action == "remind":
            return self._handle_reminder(text)
        elif action == "note":
            return self._handle_note(text)
        return "Unknown productivity command.", "english"

    def _handle_reminder(self, text):
        text_lower = text.lower()

        if "list" in text_lower or "show" in text_lower or "all" in text_lower:
            return self._list_reminders()

        if "delete" in text_lower or "remove" in text_lower or "cancel" in text_lower:
            return self._delete_reminder(text)

        task = text_lower
        for phrase in ["remind me to", "remind me", "reminder to", "याद दिला", "आठवण",
                        "remind", "reminder"]:
            task = task.replace(phrase, "").strip()

        if not task:
            return "What should I remind you about?", "english"

        minutes = None
        hours = None

        nums = re.findall(r'\d+', text_lower)

        if "minute" in text_lower or "मिनट" in text_lower:
            minutes = int(nums[0]) if nums else 5
        elif "hour" in text_lower or "घंट" in text_lower:
            hours = int(nums[0]) if nums else 1
        elif "day" in text_lower or "दिन" in text_lower:
            days = int(nums[0]) if nums else 1
            remind_at = datetime.now() + timedelta(days=days)
        else:
            minutes = 5

        if minutes:
            remind_at = datetime.now() + timedelta(minutes=minutes)
            time_str = f"{minutes} minutes"
        elif hours:
            remind_at = datetime.now() + timedelta(hours=hours)
            time_str = f"{hours} hours"
        else:
            remind_at = datetime.now() + timedelta(minutes=5)
            time_str = "5 minutes"

        reminder = {
            "id": len(self.reminders) + 1,
            "task": task,
            "remind_at": remind_at.isoformat(),
            "created": datetime.now().isoformat()
        }
        self.reminders.append(reminder)

        return f"Okay! I'll remind you to '{task}' in {time_str}.", "english"

    def _list_reminders(self):
        if not self.reminders:
            return "No reminders set.", "english"

        lines = ["Your reminders:"]
        now = datetime.now()
        for r in self.reminders:
            remind_time = datetime.fromisoformat(r["remind_at"])
            if remind_time > now:
                time_str = remind_time.strftime("%I:%M %p")
                lines.append(f"  #{r['id']}: {r['task']} at {time_str}")
            else:
                lines.append(f"  #{r['id']}: {r['task']} (due)")

        return "\n".join(lines), "english"

    def _delete_reminder(self, text):
        nums = re.findall(r'\d+', text)
        if nums:
            rem_id = int(nums[0])
            self.reminders = [r for r in self.reminders if r["id"] != rem_id]
            return f"Reminder #{rem_id} deleted.", "english"
        return "Which reminder should I delete?", "english"

    def _handle_note(self, text):
        text_lower = text.lower()

        if "list" in text_lower or "show" in text_lower or "all" in text_lower:
            return self._list_notes()

        if "delete" in text_lower or "remove" in text_lower:
            return self._delete_note(text)

        note_text = text_lower
        for phrase in ["note", "save", "लिख", "नोंद", "create note", "add note"]:
            note_text = note_text.replace(phrase, "").strip()

        if not note_text:
            return "What would you like me to note down?", "english"

        note = {
            "id": len(self.notes) + 1,
            "text": note_text,
            "created": datetime.now().isoformat()
        }
        self.notes.append(note)
        self._save_notes()

        return f"Note saved: {note_text}", "english"

    def _list_notes(self):
        if not self.notes:
            return "No notes saved.", "english"

        lines = ["Your notes:"]
        for n in self.notes:
            lines.append(f"  #{n['id']}: {n['text']}")

        return "\n".join(lines), "english"

    def _delete_note(self, text):
        nums = re.findall(r'\d+', text)
        if nums:
            note_id = int(nums[0])
            self.notes = [n for n in self.notes if n["id"] != note_id]
            self._save_notes()
            return f"Note #{note_id} deleted.", "english"
        return "Which note should I delete?", "english"
