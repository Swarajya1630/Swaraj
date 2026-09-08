"""
Swaraj Compact Floating Widget
==============================
Small floating assistant with Rajmudra at center.
Positioned top-right corner. Shows status and waveform.
"""

import tkinter as tk
import math
import time
import threading
import os


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
        self.waveform_bars = [0] * 24
        self.status_text = "STANDBY"

        self.CYAN = "#00d4ff"
        self.CYAN_DIM = "#003d55"
        self.BLUE = "#0066cc"
        self.GREEN = "#00ff88"
        self.PURPLE = "#8800ff"
        self.GOLD = "#c9a227"
        self.WHITE = "#ffffff"
        self.DARK = "#0a0a12"

        self.rajmudra_photo = None
        self._load_rajmudra()

    def _load_rajmudra(self):
        """Load the Rajmudra image for the widget."""
        asset_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "branding", "rajmudra_widget.png")
        asset_path = os.path.normpath(asset_path)

        if os.path.exists(asset_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(asset_path)
                self.rajmudra_photo = ImageTk.PhotoImage(img)
                print(f"Rajmudra loaded: {asset_path}")
            except Exception as e:
                print(f"Rajmudra load failed: {e}")
                self.rajmudra_photo = None
        else:
            print(f"Rajmudra not found: {asset_path}")

    def start(self):
        if self._running:
            return

        self._running = True
        self.root = tk.Tk()
        self.root.title("Swaraj")
        self.root.geometry("180x200")
        self.root.configure(bg=self.DARK)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.92)

        screen_w = self.root.winfo_screenwidth()
        self.root.geometry(f"180x200+{screen_w - 200}+10")

        self.canvas = tk.Canvas(
            self.root, width=180, height=200,
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
        self._dragged = False

    def _on_drag(self, event):
        dx = event.x - self._drag_x
        dy = event.y - self._drag_y
        if abs(dx) > 3 or abs(dy) > 3:
            self._dragged = True
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")

    def _on_release(self, event):
        if not self._dragged:
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

    def _get_state_color(self):
        colors = {
            "idle": self.CYAN_DIM,
            "listening": self.CYAN,
            "thinking": self.PURPLE,
            "speaking": self.GREEN,
            "error": "#ff3333"
        }
        return colors.get(self.state, self.CYAN_DIM)

    def _draw_content(self):
        if not self.canvas:
            return

        self.canvas.delete("all")

        color = self._get_state_color()

        self.canvas.create_rectangle(5, 5, 175, 195, outline=color, width=1, fill=self.DARK)

        self.canvas.create_text(90, 18, text="SWARAJ", font=("Consolas", 9, "bold"), fill=self.CYAN)

        cx, cy = 90, 95

        if self.rajmudra_photo:
            glow_intensity = 0.3 + 0.2 * math.sin(self.time * 1.5) if self.state == "idle" else 0.6 + 0.3 * math.sin(self.time * 3)

            for i in range(3, 0, -1):
                r = 55 + i * 6
                glow_color = self._adjust_alpha(color, glow_intensity * (1 - i * 0.25))
                self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=glow_color, width=1)

            ring_segments = 24
            ring_radius = 52
            for i in range(ring_segments):
                angle = (i / ring_segments) * 2 * math.pi + self.time * 0.5
                x1 = cx + ring_radius * math.cos(angle)
                y1 = cy + ring_radius * math.sin(angle)
                x2 = cx + ring_radius * math.cos(angle + 0.2)
                y2 = cy + ring_radius * math.sin(angle + 0.2)
                seg_color = color if i % 3 == 0 else self.CYAN_DIM
                self.canvas.create_line(x1, y1, x2, y2, fill=seg_color, width=1)

            self.canvas.create_image(cx, cy, image=self.rajmudra_photo)
        else:
            self.canvas.create_text(cx, cy, text="RAJMUDRA", font=("Consolas", 12, "bold"), fill=self.GOLD)

        self._draw_waveform()

        dot_size = 3 + math.sin(self.time * 3) * 1.5 if self.state != "idle" else 2
        self.canvas.create_oval(15 - dot_size, 175 - dot_size, 15 + dot_size, 175 + dot_size,
                                fill=color, outline="")
        self.canvas.create_text(25, 175, text=self.status_text, font=("Consolas", 7),
                                fill=color, anchor="w")

    def _adjust_alpha(self, hex_color, alpha):
        """Adjust color alpha for glow effects."""
        return hex_color

    def _draw_waveform(self):
        num_bars = len(self.waveform_bars)
        bar_width = 3
        spacing = 1
        total_width = num_bars * (bar_width + spacing)
        start_x = 90 - total_width // 2
        base_y = 155

        for i in range(num_bars):
            if self.state == "speaking":
                target = abs(math.sin(i * 0.5 + self.time * 8)) * 12 + 2
            elif self.state == "thinking":
                target = abs(math.sin(i * 0.4 + self.time * 4)) * 6 + 2
            elif self.state == "listening":
                target = abs(math.sin(i * 0.3 + self.time * 5)) * 5 + 2
            else:
                target = 2

            self.waveform_bars[i] += (target - self.waveform_bars[i]) * 0.3

            x = start_x + i * (bar_width + spacing)
            h = self.waveform_bars[i]
            bar_color = self.GREEN if self.state == "speaking" else \
                       self.PURPLE if self.state == "thinking" else self.CYAN_DIM

            self.canvas.create_rectangle(x, base_y - h, x + bar_width, base_y + h,
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
