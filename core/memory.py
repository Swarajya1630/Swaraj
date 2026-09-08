"""
Enhanced Memory System
=====================
Advanced memory with conversation history, preferences, context.
Separates short-term and long-term memory.
"""

import json
import os
from datetime import datetime
from core.logger import logger


class MemorySystem:
    def __init__(self):
        self.memory_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "memory")
        os.makedirs(self.memory_dir, exist_ok=True)

        self.short_term_file = os.path.join(self.memory_dir, "short_term.json")
        self.long_term_file = os.path.join(self.memory_dir, "long_term.json")
        self.preferences_file = os.path.join(self.memory_dir, "preferences.json")

        self.short_term = self._load(self.short_term_file, {"conversations": [], "context": {}})
        self.long_term = self._load(self.long_term_file, {"facts": {}, "patterns": {}, "relationships": {}})
        self.preferences = self._load(self.preferences_file, {
            "favorite_topics": [],
            "hated_topics": [],
            "greeting_style": "casual",
            "response_length": "medium",
            "language": "english"
        })

    def _load(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return default

    def _save(self, path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_all(self):
        self._save(self.short_term_file, self.short_term)
        self._save(self.long_term_file, self.long_term)
        self._save(self.preferences_file, self.preferences)

    def add_conversation(self, user_msg, swaraj_response):
        entry = {
            "time": datetime.now().isoformat(),
            "user": user_msg,
            "swaraj": swaraj_response
        }
        self.short_term["conversations"].append(entry)

        if len(self.short_term["conversations"]) > 100:
            self.short_term["conversations"] = self.short_term["conversations"][-100:]

        self._extract_facts(user_msg)
        self.save_all()

    def _extract_facts(self, text):
        text_lower = text.lower()

        patterns = [
            (r"my name is (\w+)", "owner_name"),
            (r"i am (\d+) (?:years old|yo)", "age"),
            (r"i live in (\w+)", "city"),
            (r"i work as (\w+)", "job"),
            (r"my favorite (\w+) is (.+)", "favorite_{0}"),
            (r"i (?:like|love) (.+)", "likes"),
            (r"i (?:hate|dislike) (.+)", "dislikes"),
        ]

        import re
        for pattern, key in patterns:
            match = re.search(pattern, text_lower)
            if match:
                if "{0}" in key:
                    key = key.format(match.group(1))
                    value = match.group(2)
                else:
                    value = match.group(1)

                self.long_term["facts"][key] = value
                logger.debug(f"Learned fact: {key} = {value}")

    def set_context(self, key, value):
        self.short_term["context"][key] = value
        self.save_all()

    def get_context(self, key=None):
        if key:
            return self.short_term["context"].get(key)
        return self.short_term["context"]

    def get_recent_conversations(self, n=10):
        return self.short_term["conversations"][-n:]

    def set_preference(self, key, value):
        self.preferences[key] = value
        self.save_all()

    def get_preference(self, key, default=None):
        return self.preferences.get(key, default)

    def learn_pattern(self, pattern_type, pattern):
        if pattern_type not in self.long_term["patterns"]:
            self.long_term["patterns"][pattern_type] = []
        if pattern not in self.long_term["patterns"][pattern_type]:
            self.long_term["patterns"][pattern_type].append(pattern)
            self.save_all()

    def get_patterns(self, pattern_type):
        return self.long_term["patterns"].get(pattern_type, [])

    def add_relationship(self, entity, relation, value):
        if entity not in self.long_term["relationships"]:
            self.long_term["relationships"][entity] = {}
        self.long_term["relationships"][entity][relation] = value
        self.save_all()

    def get_relationship(self, entity):
        return self.long_term["relationships"].get(entity, {})

    def get_context_string(self):
        context_parts = []

        if self.long_term["facts"]:
            context_parts.append(f"Facts: {json.dumps(self.long_term['facts'], ensure_ascii=False)}")

        if self.preferences:
            context_parts.append(f"Preferences: {json.dumps(self.preferences, ensure_ascii=False)}")

        recent = self.get_recent_conversations(5)
        if recent:
            conv_str = "; ".join([f"User: {c['user'][:50]}" for c in recent])
            context_parts.append(f"Recent: {conv_str}")

        return "\n".join(context_parts) if context_parts else "No context available."

    def clear_short_term(self):
        self.short_term = {"conversations": [], "context": {}}
        self.save_all()

    def clear_all(self):
        self.short_term = {"conversations": [], "context": {}}
        self.long_term = {"facts": {}, "patterns": {}, "relationships": {}}
        self.preferences = {
            "favorite_topics": [],
            "hated_topics": [],
            "greeting_style": "casual",
            "response_length": "medium",
            "language": "english"
        }
        self.save_all()

    def get_stats(self):
        return {
            "conversations": len(self.short_term["conversations"]),
            "facts": len(self.long_term["facts"]),
            "patterns": sum(len(v) for v in self.long_term["patterns"].values()),
            "relationships": len(self.long_term["relationships"])
        }
