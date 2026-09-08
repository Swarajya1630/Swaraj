"""
Email and Calendar Integration
==============================
Basic email and calendar features using local storage.
Supports ICS calendar files and email templates.
"""

import os
import json
import re
from datetime import datetime, timedelta
from core.logger import logger


class EmailCalendarModule:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "calendar")
        os.makedirs(self.data_dir, exist_ok=True)

        self.events_file = os.path.join(self.data_dir, "events.json")
        self.events = self._load_events()

        self.contacts_file = os.path.join(self.data_dir, "contacts.json")
        self.contacts = self._load_contacts()

    def _load_events(self):
        if os.path.exists(self.events_file):
            try:
                with open(self.events_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_events(self):
        with open(self.events_file, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)

    def _load_contacts(self):
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_contacts(self):
        with open(self.contacts_file, "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, indent=2, ensure_ascii=False)

    def add_event(self, title, date_str, time_str="09:00", duration_hours=1, description=""):
        """Add a calendar event."""
        try:
            event_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                event_datetime = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            except ValueError:
                return None, "Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY"

        event = {
            "id": len(self.events) + 1,
            "title": title,
            "datetime": event_datetime.isoformat(),
            "duration_hours": duration_hours,
            "description": description,
            "created": datetime.now().isoformat()
        }

        self.events.append(event)
        self._save_events()

        return event["id"], f"Event '{title}' added for {event_datetime.strftime('%B %d, %Y at %I:%M %p')}"

    def get_events(self, date_str=None):
        """Get events for a specific date or all events."""
        if date_str:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                try:
                    target_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                except:
                    return self.events

            filtered = []
            for event in self.events:
                event_date = datetime.fromisoformat(event["datetime"]).date()
                if event_date == target_date:
                    filtered.append(event)
            return filtered

        return self.events

    def get_upcoming(self, days=7):
        """Get upcoming events within specified days."""
        now = datetime.now()
        cutoff = now + timedelta(days=days)

        upcoming = []
        for event in self.events:
            event_dt = datetime.fromisoformat(event["datetime"])
            if now <= event_dt <= cutoff:
                upcoming.append(event)

        upcoming.sort(key=lambda e: e["datetime"])
        return upcoming

    def delete_event(self, event_id):
        """Delete an event by ID."""
        self.events = [e for e in self.events if e["id"] != event_id]
        self._save_events()

    def add_contact(self, name, email="", phone=""):
        """Add a contact."""
        contact = {
            "id": len(self.contacts) + 1,
            "name": name,
            "email": email,
            "phone": phone,
            "created": datetime.now().isoformat()
        }

        self.contacts.append(contact)
        self._save_contacts()

        return contact["id"], f"Contact '{name}' added"

    def get_contact(self, name):
        """Search contacts by name."""
        name_lower = name.lower()
        return [c for c in self.contacts if name_lower in c["name"].lower()]

    def format_events(self, events):
        """Format events for display."""
        if not events:
            return "No events found."

        lines = ["Calendar Events:"]
        for event in events:
            dt = datetime.fromisoformat(event["datetime"])
            lines.append(f"  #{event['id']}: {event['title']} - {dt.strftime('%B %d at %I:%M %p')}")

        return "\n".join(lines)

    def format_contacts(self, contacts):
        """Format contacts for display."""
        if not contacts:
            return "No contacts found."

        lines = ["Contacts:"]
        for c in contacts:
            lines.append(f"  {c['name']}: {c.get('email', 'N/A')} | {c.get('phone', 'N/A')}")

        return "\n".join(lines)
