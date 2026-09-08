"""
Swaraj Settings Window
=====================
Full settings interface for configuring Swaraj.
Access via system tray or expanded window.
"""

import tkinter as tk
from tkinter import ttk
import os
from core.logger import logger


class SettingsWindow:
    def __init__(self, app=None):
        self.app = app
        self.root = None
        self._visible = False

        self.CYAN = "#00d4ff"
        self.CYAN_DIM = "#003d55"
        self.GREEN = "#00ff88"
        self.PURPLE = "#8800ff"
        self.WHITE = "#ffffff"
        self.DARK = "#0a0a12"
        self.DARK2 = "#0f0f1a"

    def show(self):
        if self._visible and self.root:
            self.root.lift()
            return

        self._visible = True
        self.root = tk.Tk()
        self.root.title("SWARAJ - Settings")
        self.root.geometry("600x700")
        self.root.configure(bg=self.DARK)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        screen_w = self.root.winfo_screenwidth()
        x = (screen_w - 600) // 2
        y = 100
        self.root.geometry(f"600x700+{x}+{y}")

        self._setup_ui()

    def _setup_ui(self):
        header = tk.Frame(self.root, bg=self.DARK2, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="SWARAJ SETTINGS", font=("Consolas", 14, "bold"),
                 fg=self.CYAN, bg=self.DARK2).pack(pady=15)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        general_frame = tk.Frame(notebook, bg=self.DARK)
        notebook.add(general_frame, text="  General  ")
        self._setup_general_tab(general_frame)

        voice_frame = tk.Frame(notebook, bg=self.DARK)
        notebook.add(voice_frame, text="  Voice  ")
        self._setup_voice_tab(voice_frame)

        ai_frame = tk.Frame(notebook, bg=self.DARK)
        notebook.add(ai_frame, text="  AI  ")
        self._setup_ai_tab(ai_frame)

        appearance_frame = tk.Frame(notebook, bg=self.DARK)
        notebook.add(appearance_frame, text="  Appearance  ")
        self._setup_appearance_tab(appearance_frame)

        about_frame = tk.Frame(notebook, bg=self.DARK)
        notebook.add(about_frame, text="  About  ")
        self._setup_about_tab(about_frame)

    def _setup_general_tab(self, parent):
        config = self.app.config if self.app else {}

        self.startup_var = tk.BooleanVar(value=config.get("general", "start_with_windows", True))
        self.minimized_var = tk.BooleanVar(value=config.get("general", "start_minimized", True))
        self.topmost_var = tk.BooleanVar(value=config.get("general", "always_on_top", True))

        items = [
            ("Start SWARAJ with Windows", self.startup_var, "start_with_windows"),
            ("Start minimized to tray", self.minimized_var, "start_minimized"),
            ("Always on top", self.topmost_var, "always_on_top"),
        ]

        for i, (label, var, key) in enumerate(items):
            frame = tk.Frame(parent, bg=self.DARK)
            frame.pack(fill="x", padx=20, pady=10)

            cb = tk.Checkbutton(frame, text=label, variable=var,
                                font=("Consolas", 10), fg=self.WHITE, bg=self.DARK,
                                selectcolor=self.DARK2, activebackground=self.DARK,
                                activeforeground=self.WHITE,
                                command=lambda k=key, v=var: self._on_setting_change(k, v))
            cb.pack(anchor="w")

        lang_frame = tk.Frame(parent, bg=self.DARK)
        lang_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(lang_frame, text="Language:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK).pack(anchor="w")

        self.lang_var = tk.StringVar(value=config.get("general", "language", "english"))
        lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                  values=["english", "hindi", "marathi"], state="readonly")
        lang_menu.pack(anchor="w", pady=5)
        lang_menu.bind("<<ComboboxSelected>>", lambda e: self._on_setting_change("language", self.lang_var))

    def _setup_voice_tab(self, parent):
        config = self.app.config if self.app else {}

        self.wake_enabled_var = tk.BooleanVar(value=config.get("voice", "wake_word_enabled", True))

        tk.Checkbutton(parent, text="Enable Wake Word", variable=self.wake_enabled_var,
                        font=("Consolas", 10), fg=self.WHITE, bg=self.DARK,
                        selectcolor=self.DARK2, activebackground=self.DARK,
                        command=lambda: self._on_setting_change("wake_word_enabled", self.wake_enabled_var)).pack(anchor="w", padx=20, pady=10)

        rate_frame = tk.Frame(parent, bg=self.DARK)
        rate_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(rate_frame, text="Speech Rate:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK).pack(anchor="w")

        self.rate_var = tk.IntVar(value=config.get("voice", "speech_rate", 175))
        rate_scale = tk.Scale(rate_frame, from_=100, to=250, variable=self.rate_var,
                               orient="horizontal", length=400, bg=self.DARK, fg=self.WHITE,
                               troughcolor=self.DARK2, highlightthickness=0,
                               command=lambda v: self._on_setting_change("speech_rate", self.rate_var))
        rate_scale.pack(anchor="w")

        vol_frame = tk.Frame(parent, bg=self.DARK)
        vol_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(vol_frame, text="Volume:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK).pack(anchor="w")

        self.vol_var = tk.DoubleVar(value=config.get("voice", "volume", 0.9))
        vol_scale = tk.Scale(vol_frame, from_=0.0, to=1.0, resolution=0.1,
                              variable=self.vol_var, orient="horizontal", length=400,
                              bg=self.DARK, fg=self.WHITE, troughcolor=self.DARK2,
                              highlightthickness=0,
                              command=lambda v: self._on_setting_change("volume", self.vol_var))
        vol_scale.pack(anchor="w")

    def _setup_ai_tab(self, parent):
        config = self.app.config if self.app else {}

        model_frame = tk.Frame(parent, bg=self.DARK)
        model_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(model_frame, text="AI Model:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK).pack(anchor="w")

        self.model_var = tk.StringVar(value=config.get("ai", "model", "mistral"))
        model_menu = ttk.Combobox(model_frame, textvariable=self.model_var,
                                   values=["mistral", "llama3.2", "codellama", "phi3"],
                                   state="readonly")
        model_menu.pack(anchor="w", pady=5)
        model_menu.bind("<<ComboboxSelected>>", lambda e: self._on_setting_change("model", self.model_var))

        temp_frame = tk.Frame(parent, bg=self.DARK)
        temp_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(temp_frame, text="Temperature:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK).pack(anchor="w")

        self.temp_var = tk.DoubleVar(value=config.get("ai", "temperature", 0.8))
        temp_scale = tk.Scale(temp_frame, from_=0.0, to=1.5, resolution=0.1,
                               variable=self.temp_var, orient="horizontal", length=400,
                               bg=self.DARK, fg=self.WHITE, troughcolor=self.DARK2,
                               highlightthickness=0,
                               command=lambda v: self._on_setting_change("temperature", self.temp_var))
        temp_scale.pack(anchor="w")

        status_frame = tk.Frame(parent, bg=self.DARK2, relief="flat")
        status_frame.pack(fill="x", padx=20, pady=20)

        ai_status = "Connected" if (self.app and self.app.ai_brain) else "Offline"
        ai_color = self.GREEN if ai_status == "Connected" else "#ff3333"

        tk.Label(status_frame, text="AI Status:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK2).pack(anchor="w", padx=10, pady=5)
        tk.Label(status_frame, text=ai_status, font=("Consolas", 10, "bold"),
                 fg=ai_color, bg=self.DARK2).pack(anchor="w", padx=10)

    def _setup_appearance_tab(self, parent):
        config = self.app.config if self.app else {}

        self.opacity_var = tk.DoubleVar(value=config.get("appearance", "widget_opacity", 0.92))

        op_frame = tk.Frame(parent, bg=self.DARK)
        op_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(op_frame, text="Widget Opacity:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK).pack(anchor="w")

        op_scale = tk.Scale(op_frame, from_=0.5, to=1.0, resolution=0.05,
                             variable=self.opacity_var, orient="horizontal", length=400,
                             bg=self.DARK, fg=self.WHITE, troughcolor=self.DARK2,
                             highlightthickness=0,
                             command=lambda v: self._on_setting_change("widget_opacity", self.opacity_var))
        op_scale.pack(anchor="w")

        intensity_frame = tk.Frame(parent, bg=self.DARK)
        intensity_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(intensity_frame, text="Animation Intensity:", font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK).pack(anchor="w")

        self.intensity_var = tk.StringVar(value=config.get("appearance", "animation_intensity", "medium"))
        intensity_menu = ttk.Combobox(intensity_frame, textvariable=self.intensity_var,
                                       values=["low", "medium", "high"], state="readonly")
        intensity_menu.pack(anchor="w", pady=5)
        intensity_menu.bind("<<ComboboxSelected>>", lambda e: self._on_setting_change("animation_intensity", self.intensity_var))

    def _setup_about_tab(self, parent):
        about_text = """
S W A R A J

Smart Wide-purpose Automated Reasoning
And Assistance Junction

Your personal AI best friend.
Inspired by Chhatrapati Shivaji Maharaj.

Only YOU can talk to Swaraj.

Built with:
- Python
- Ollama (Local AI)
- Rajmudra Visual Identity

Version: 1.0.0
        """

        tk.Label(parent, text=about_text, font=("Consolas", 10),
                 fg=self.WHITE, bg=self.DARK, justify="center").pack(expand=True)

    def _on_setting_change(self, key, var):
        if not self.app:
            return

        value = var.get() if hasattr(var, 'get') else var

        section_map = {
            "start_with_windows": "general",
            "start_minimized": "general",
            "always_on_top": "general",
            "language": "general",
            "wake_word_enabled": "voice",
            "speech_rate": "voice",
            "volume": "voice",
            "model": "ai",
            "temperature": "ai",
            "widget_opacity": "appearance",
            "animation_intensity": "appearance",
        }

        section = section_map.get(key, "general")
        self.app.config.set(section, key, value)
        logger.info(f"Setting changed: {key} = {value}")

    def hide(self):
        self._visible = False
        if self.root:
            self.root.withdraw()

    def stop(self):
        self._visible = False
        if self.root:
            self.root.after(100, self.root.destroy)
