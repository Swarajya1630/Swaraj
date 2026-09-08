"""
Compact Floating Widget
======================
Small floating assistant in top-right corner.
Shows status, waveform, and listening state.
"""

import tkinter as tk
import math
import time
import threading


class CompactWidget:
    def __init__(self, app=None):
        self.app = app
        self.root = None
        self.canvas = None
        self._running = False
        self._expanded = False
        self.expanded_window = None

        self.state = "idle"
        self.time = 0
        self.pulse = 0
        self.waveform_bars = [0] * 16
        self.status_text = "STANDBY"

        self.CYAN = "#00d4ff"
        self.CYAN_DIM = "#004466"
        self.BLUE = "#0066cc"
        self.GREEN = "#00ff88"
        self.PURPLE = "#8800ff"
        self.WHITE = "#ffffff"
        self.DARK = "#0a0a12"

    def start(self):
        if self._running:
            return

        self._running = True
        self.root = tk.Tk()
        self.root.title("Swaraj")
        self.root.geometry("220x120")
        self.root.configure(bg=self.DARK)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.92)

        screen_w = self.root.winfo_screenwidth()
        self.root.geometry(f"220x120+{screen_w - 240}+10")

        self.canvas = tk.Canvas(
            self.root, width=220, height=120,
            bg=self.DARK, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        self._draw_content()
        self._animate()

    def _on_click(self, event):
        self._drag_x = event.x
        self._drag_y = event.y
        self._click_start_time = time.time()

    def _on_release(self, event):
        elapsed = time.time() - self._click_start_time
        if elapsed < 0.3 and abs(event.x - self._drag_x) < 5:
            self._toggle_expanded()

    def _toggle_expanded(self):
        if self.expanded_window and self.expanded_window._visible:
            self.expanded_window.hide()
        else:
            self._show_expanded()

    def _show_expanded(self):
        if not self.expanded_window:
            from ui.expanded.window import ExpandedWindow
            self.expanded_window = ExpandedWindow(self.app)
            if self.app:
                self.expanded_window.on_send = self.app._process_command_ui
        self.expanded_window.show()

    def _on_drag(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def _draw_content(self):
        if not self.canvas:
            return

        self.canvas.delete("all")

        state_colors = {
            "idle": self.CYAN_DIM,
            "listening": self.CYAN,
            "thinking": self.PURPLE,
            "speaking": self.GREEN
        }
        color = state_colors.get(self.state, self.CYAN_DIM)

        self.canvas.create_rectangle(5, 5, 215, 115, outline=color, width=1, fill=self.DARK)

        self.canvas.create_text(110, 15, text="SWARAJ", font=("Consolas", 9, "bold"), fill=self.CYAN)

        dot_size = 3 + math.sin(self.time * 3) * 1.5 if self.state != "idle" else 2
        self.canvas.create_oval(20 - dot_size, 30 - dot_size, 20 + dot_size, 30 + dot_size,
                                fill=color, outline="")
        self.canvas.create_text(30, 30, text=self.status_text, font=("Consolas", 8),
                                fill=color, anchor="w")

        self._draw_mini_waveform()

        if self.state == "listening":
            self.canvas.create_text(110, 105, text="Listening...", font=("Consolas", 7),
                                    fill=self.CYAN)
        elif self.state == "thinking":
            self.canvas.create_text(110, 105, text="Thinking...", font=("Consolas", 7),
                                    fill=self.PURPLE)
        elif self.state == "speaking":
            self.canvas.create_text(110, 105, text="Speaking...", font=("Consolas", 7),
                                    fill=self.GREEN)

    def _draw_mini_waveform(self):
        num_bars = len(self.waveform_bars)
        bar_width = 4
        spacing = 2
        total_width = num_bars * (bar_width + spacing)
        start_x = 110 - total_width // 2

        for i in range(num_bars):
            if self.state == "speaking":
                target = abs(math.sin(i * 0.5 + self.time * 6)) * 15 + 2
            elif self.state == "thinking":
                target = abs(math.sin(i * 0.4 + self.time * 3)) * 8 + 2
            elif self.state == "listening":
                target = abs(math.sin(i * 0.3 + self.time * 4)) * 5 + 2
            else:
                target = 2

            self.waveform_bars[i] += (target - self.waveform_bars[i]) * 0.3

            x = start_x + i * (bar_width + spacing)
            h = self.waveform_bars[i]
            bar_color = self.GREEN if self.state == "speaking" else \
                       self.PURPLE if self.state == "thinking" else self.CYAN_DIM

            self.canvas.create_rectangle(x, 70 - h, x + bar_width, 70 + h,
                                         fill=bar_color, outline="")

    def _animate(self):
        if not self._running:
            return

        self.time += 0.05
        self.pulse = math.sin(self.time * 2)
        self._draw_content()
        self.root.after(50, self._animate)

    def set_state(self, state):
        self.state = state

    def set_status(self, text):
        self.status_text = text

    def stop(self):
        self._running = False
        if self.root:
            self.root.after(100, self.root.destroy)
