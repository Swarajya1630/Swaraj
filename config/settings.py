"""
Configuration System
===================
Centralized settings with file persistence.
All SWARAJ settings live here.
"""

import json
import os


DEFAULT_CONFIG = {
    "general": {
        "start_with_windows": True,
        "start_minimized": True,
        "always_on_top": True,
        "language": "english"
    },
    "voice": {
        "wake_word_enabled": True,
        "wake_words": ["hey swaraj", "swaraj"],
        "microphone_index": None,
        "energy_threshold": 4000,
        "speech_rate": 175,
        "volume": 0.9,
        "voice_index": 0
    },
    "ai": {
        "provider": "ollama",
        "model": "mistral",
        "ollama_url": "http://localhost:11434",
        "temperature": 0.8,
        "max_tokens": 200
    },
    "appearance": {
        "theme": "dark",
        "widget_size": "compact",
        "widget_opacity": 0.95,
        "animation_intensity": "medium",
        "position_x": -1,
        "position_y": -1,
        "monitor": 0
    },
    "privacy": {
        "wake_word_local": True,
        "log_commands": False,
        "save_conversations": True
    }
}


class Config:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
            self.config_file = os.path.join(self.config_dir, "settings.json")
            self._config = self._load()

    def _load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    loaded = json.load(f)
                return self._merge(DEFAULT_CONFIG, loaded)
            except:
                pass
        return DEFAULT_CONFIG.copy()

    def _merge(self, defaults, overrides):
        result = defaults.copy()
        for key, value in overrides.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge(result[key], value)
            else:
                result[key] = value
        return result

    def save(self):
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self._config, f, indent=2)

    def get(self, section, key=None, default=None):
        if key is None:
            return self._config.get(section, default)
        return self._config.get(section, {}).get(key, default)

    def set(self, section, key, value):
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        self.save()

    def __getitem__(self, key):
        return self._config[key]
