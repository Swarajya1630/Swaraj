"""
Personal Identity Module
========================
Makes Swaraj YOUR personal best friend.
- Only you can talk to Swaraj
- Stores your name, preferences, and memories
- Refuses to interact with others
- Learns your habits and personality over time
"""

import json
import os
from datetime import datetime


class PersonalIdentity:
    def __init__(self, data_file="swaraj_memory.json"):
        self.data_file = os.path.join(os.path.dirname(__file__), data_file)
        self.data = self._load_data()

    def _get_default_data(self):
        """Return default data structure."""
        return {
            "owner": {
                "name": "",
                "nickname": "",
                "is_trained": False,
                "voice_registered": False
            },
            "personality": {
                "sarcasm_level": 0.5,
                "formality": 0.3,
                "humor": 0.7,
                "verbosity": 0.5,
                "empathy": 0.8
            },
            "preferences": {
                "favorite_topics": [],
                "hated_topics": [],
                "greeting_style": "casual",
                "response_length": "medium"
            },
            "memories": {
                "conversations": [],
                "important_facts": {},
                "mood_history": []
            },
            "friendship": {
                "level": 1,
                "xp": 0,
                "started": "",
                "total_conversations": 0,
                "inside_jokes": [],
                "nicknames_for_user": ["shiva", "bro", "yaar", "dude", "friend"]
            },
            "bookmarks": {}
        }

    def _load_data(self):
        """Load saved data from file, merging with defaults for missing keys."""
        default = self._get_default_data()
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                # Merge loaded data with defaults (fills missing keys)
                for key in default:
                    if key not in loaded:
                        loaded[key] = default[key]
                    elif isinstance(default[key], dict):
                        for subkey in default[key]:
                            if subkey not in loaded[key]:
                                loaded[key][subkey] = default[key][subkey]
                return loaded
            except json.JSONDecodeError:
                return default
        return default

    def _save_data(self):
        """Save data to file."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def is_owner(self, name_or_input):
        """Check if the person is the owner."""
        if not self.data["owner"]["is_trained"]:
            return True  # Not trained yet, accept anyone
        name_lower = name_or_input.lower().strip()
        owner_name = self.data["owner"]["name"].lower()
        nickname = self.data["owner"]["nickname"].lower()
        return name_lower == owner_name or name_lower == nickname or owner_name in name_lower

    def setup_owner(self, name, nickname=""):
        """First-time setup - register the owner."""
        self.data["owner"]["name"] = name
        self.data["owner"]["nickname"] = nickname or name
        self.data["owner"]["is_trained"] = True
        self.data["friendship"]["started"] = datetime.now().isoformat()
        self._save_data()
        return f"Nice to meet you, {name}! You're now my best friend forever."

    def get_owner_name(self):
        """Get the owner's name."""
        return self.data["owner"]["name"]

    def get_nickname(self):
        """Get owner's nickname."""
        return self.data["owner"]["nickname"] or self.data["owner"]["name"]

    def learn_fact(self, key, value):
        """Remember something about the owner."""
        self.data["memories"]["important_facts"][key] = value
        self._save_data()

    def get_fact(self, key):
        """Recall a fact about the owner."""
        return self.data["memories"]["important_facts"].get(key, None)

    def add_conversation(self, user_msg, swaraj_response):
        """Store conversation for memory."""
        conv = {
            "time": datetime.now().isoformat(),
            "user": user_msg,
            "swaraj": swaraj_response
        }
        self.data["memories"]["conversations"].append(conv)
        # Keep only last 50 conversations
        if len(self.data["memories"]["conversations"]) > 50:
            self.data["memories"]["conversations"] = \
                self.data["memories"]["conversations"][-50:]
        self._save_data()

    def add_inside_joke(self, joke):
        """Add an inside joke."""
        self.data["friendship"]["inside_jokes"].append(joke)
        self._save_data()

    def get_random_nickname(self):
        """Get a random friendly nickname for the user."""
        import random
        nicknames = self.data["friendship"]["nicknames_for_user"]
        return random.choice(nicknames) if nicknames else "friend"

    def add_xp(self, amount=10):
        """Add friendship XP."""
        self.data["friendship"]["xp"] += amount
        old_level = self.data["friendship"]["level"]
        # Level up every 100 XP
        self.data["friendship"]["level"] = \
            1 + self.data["friendship"]["xp"] // 100
        new_level = self.data["friendship"]["level"]
        self.data["friendship"]["total_conversations"] += 1
        self._save_data()
        if new_level > old_level:
            return f"Friendship level up! Now level {new_level}!"
        return None

    def set_personality_trait(self, trait, value):
        """Adjust Swaraj's personality."""
        if trait in self.data["personality"]:
            self.data["personality"][trait] = max(0.0, min(1.0, value))
            self._save_data()

    def set_preference(self, key, value):
        """Set a user preference."""
        self.data["preferences"][key] = value
        self._save_data()

    def add_bookmark(self, name, url):
        """Save a website bookmark with a custom name."""
        if not url.startswith("http"):
            url = "https://" + url
        self.data["bookmarks"][name.lower()] = url
        self._save_data()

    def get_bookmark(self, name):
        """Get URL by bookmark name."""
        return self.data["bookmarks"].get(name.lower(), None)

    def remove_bookmark(self, name):
        """Remove a bookmark."""
        if name.lower() in self.data["bookmarks"]:
            del self.data["bookmarks"][name.lower()]
            self._save_data()
            return True
        return False

    def list_bookmarks(self):
        """List all saved bookmarks."""
        return self.data["bookmarks"]

    def get_context_string(self):
        """Get context about the owner for the AI brain."""
        facts = self.data["memories"]["important_facts"]
        personality = self.data["personality"]
        friendship = self.data["friendship"]

        context = f"\n[OWNER INFO]\n"
        context += f"Name: {self.data['owner']['name']}\n"
        context += f"Friendship Level: {friendship['level']}\n"
        context += f"Total conversations: {friendship['total_conversations']}\n"

        if facts:
            context += f"Facts about owner: {json.dumps(facts, ensure_ascii=False)}\n"

        context += f"Personality: sarcasm={personality['sarcasm_level']}, "
        context += f"humor={personality['humor']}, "
        context += f"empathy={personality['empathy']}\n"

        if friendship['inside_jokes']:
            context += f"Inside jokes: {friendship['inside_jokes'][-3:]}\n"

        if self.data["bookmarks"]:
            context += f"Bookmarks: {json.dumps(self.data['bookmarks'], ensure_ascii=False)}\n"

        return context
