"""
Swaraj UI - Jarvis-Grade Interface with Weather Dashboard
=========================================================
Rajmudra startup, arc reactor, weather, agent status, waveform.
"""

import tkinter as tk
import math
import time
import threading
import random
import os


class SwarajUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SWARAJ")
        self.root.geometry("700x750")
        self.root.configure(bg="#000000")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        # Colors
        self.CYAN = "#00d4ff"
        self.CYAN_DIM = "#005577"
        self.BLUE = "#0066cc"
        self.PURPLE = "#8800ff"
        self.GREEN = "#00ff88"
        self.WHITE = "#ffffff"
        self.DARK = "#000000"
        self.GOLD = "#c9a227"
        self.ORANGE = "#ff8800"
        self.RED = "#ff3333"

        # State
        self.state = "startup"
        self.time = 0
        self.pulse = 0
        self.startup_stage = 0
        self.particles = []
        self.agent_status = "STANDBY"
        self.weather_data = {"main": "--", "condition": "--", "details": "--", "city": "--"}
        self.waveform_bars = [0] * 32

        # Load Rajmudra
        self.has_image = False
        self._load_rajmudra()

        # Start weather updates
        self._start_weather_thread()

        self._setup_ui()
        self._init_particles()
        self._animate()

    def _load_rajmudra(self):
        img_path = os.path.join(os.path.dirname(__file__), "assets", "rajmudra.png")
        if os.path.exists(img_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(img_path)
                img = img.resize((280, 280), Image.Resampling.LANCZOS)
                self.rajmudra_photo = ImageTk.PhotoImage(img)
                self.has_image = True
            except Exception:
                self.has_image = False

    def _start_weather_thread(self):
        def fetch():
            try:
                from weather import Weather
                w = Weather()
                data = w.get_weather("auto")
                self.weather_data = w.format_display(data)
            except Exception:
                self.weather_data = {"main": "--", "condition": "Offline", "details": "--", "city": "--"}
        threading.Thread(target=fetch, daemon=True).start()
        # Refresh every 10 minutes
        self.root.after(600000, self._start_weather_thread)

    def _setup_ui(self):
        self.canvas = tk.Canvas(
            self.root, width=700, height=750,
            bg=self.DARK, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Response area
        self.canvas.create_rectangle(50, 620, 650, 710, fill="#050a10", outline=self.CYAN_DIM, width=1)
        self.response_label = self.canvas.create_text(
            350, 665, text="", font=("Consolas", 10), fill=self.WHITE, width=580
        )

        # Input
        self.input_frame = tk.Frame(self.root, bg="#050a10")
        self.input_frame.place(x=60, y=715, width=480, height=30)
        self.input_entry = tk.Entry(
            self.input_frame, font=("Consolas", 10), bg="#0a1020",
            fg=self.CYAN, insertbackground=self.CYAN, relief="flat"
        )
        self.input_entry.pack(fill="both", expand=True, padx=2, pady=2)
        self.input_entry.bind("<Return>", self._on_send)

        self.send_btn = tk.Canvas(self.root, width=80, height=30, bg="#0a1020", highlightthickness=0, cursor="hand2")
        self.send_btn.place(x=550, y=717)
        self.send_btn.create_text(40, 15, text="SEND", font=("Consolas", 9, "bold"), fill=self.CYAN)
        self.send_btn.bind("<Button-1>", lambda e: self._on_send(None))

        self.on_send = None

    def _init_particles(self):
        for _ in range(40):
            self.particles.append({
                "x": random.randint(50, 650), "y": random.randint(80, 600),
                "vx": random.uniform(-0.2, 0.2), "vy": random.uniform(-0.3, 0.1),
                "size": random.uniform(0.5, 1.5)
            })

    def _draw_grid(self):
        for x in range(0, 700, 40):
            self.canvas.create_line(x, 60, x, 610, fill="#060d15", width=1)
        for y in range(60, 610, 40):
            self.canvas.create_line(0, y, 700, y, fill="#060d15", width=1)

    def _draw_startup(self):
        cx, cy = 350, 300
        t = self.time

        if self.has_image:
            glow_size = 170 + math.sin(t * 2) * 10
            for i in range(5, 0, -1):
                r = glow_size + i * 8
                self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=self.GOLD, width=1)
            self.canvas.create_image(cx, cy, image=self.rajmudra_photo)

            for ring in range(3):
                r = 165 + ring * 15
                segments = 20 + ring * 4
                speed = (1 + ring * 0.5) * (1 if ring % 2 == 0 else -1)
                for i in range(segments):
                    angle = (i / segments) * 2 * math.pi + t * speed
                    x1 = cx + r * math.cos(angle)
                    y1 = cy + r * math.sin(angle)
                    x2 = cx + r * math.cos(angle + 0.3)
                    y2 = cy + r * math.sin(angle + 0.3)
                    self.canvas.create_line(x1, y1, x2, y2, fill=self.GOLD, width=1)
        else:
            self.canvas.create_text(cx, cy, text="RAJMUDRA", font=("Consolas", 24, "bold"), fill=self.GOLD)

        self.canvas.create_text(cx, 500, text="S W A R A J", font=("Consolas", 18, "bold"), fill=self.GOLD)
        self.canvas.create_text(cx, 530, text="चत्रपती शिवाजी महाराजांच्या आदर्शावर",
                                font=("Consolas", 11), fill=self.CYAN_DIM)

        # Loading bar
        progress = min(1.0, (t - 1) / 4)
        bar_x, bar_y, bar_w = 200, 570, 300
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + 8, outline=self.CYAN_DIM, width=1)
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w * progress, bar_y + 8, fill=self.CYAN, outline="")

        if progress >= 1.0:
            self.canvas.create_text(cx, 590, text="SYSTEMS ONLINE", font=("Consolas", 9), fill=self.GREEN)

    def _draw_arc_reactor(self, cx, cy):
        t = self.time
        state_colors = {"idle": self.CYAN_DIM, "listening": self.CYAN, "thinking": self.PURPLE, "speaking": self.GREEN}
        glow_color = state_colors.get(self.state, self.CYAN_DIM)

        # Outer glow
        for i in range(15, 0, -1):
            r = 80 + i * 4 + self.pulse * 3
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=glow_color, width=1)

        # Ring 1 - Outer
        for i in range(24):
            angle = (i / 24) * 2 * math.pi + t * 0.5
            x1 = cx + 100 * math.cos(angle)
            y1 = cy + 100 * math.sin(angle)
            x2 = cx + 100 * math.cos(angle + 0.3)
            y2 = cy + 100 * math.sin(angle + 0.3)
            if i % 2 == 0:
                self.canvas.create_line(x1, y1, x2, y2, fill=self.CYAN, width=2)

        # Ring 2 - Middle
        for i in range(16):
            angle = (i / 16) * 2 * math.pi - t * 0.8
            x1 = cx + 75 * math.cos(angle)
            y1 = cy + 75 * math.sin(angle)
            x2 = cx + 75 * math.cos(angle + 0.25)
            y2 = cy + 75 * math.sin(angle + 0.25)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.BLUE, width=2)

        # Ring 3 - Inner
        for i in range(12):
            angle = (i / 12) * 2 * math.pi + t * 1.2
            x1 = cx + 50 * math.cos(angle)
            y1 = cy + 50 * math.sin(angle)
            x2 = cx + 50 * math.cos(angle + 0.4)
            y2 = cy + 50 * math.sin(angle + 0.4)
            color = self.PURPLE if self.state == "thinking" else self.CYAN
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        # Core
        core_size = 20 + self.pulse * 5
        core_colors = {"idle": self.CYAN, "listening": "#00ffff", "thinking": "#aa44ff", "speaking": "#00ff88"}
        self.canvas.create_oval(cx-core_size, cy-core_size, cx+core_size, cy+core_size,
                                fill=core_colors.get(self.state, self.CYAN), outline=self.WHITE, width=1)
        inner = core_size * 0.5
        self.canvas.create_oval(cx-inner, cy-inner, cx+inner, cy+inner, fill="#ffffff", outline="")

    def _draw_weather_dashboard(self):
        """Draw weather info on top-right."""
        x, y = 520, 80
        self.canvas.create_rectangle(x-10, y-15, x+120, y+60, fill="#050a10", outline=self.CYAN_DIM, width=1)
        self.canvas.create_text(x, y-5, text="WEATHER", font=("Consolas", 7), fill=self.CYAN_DIM, anchor="w")
        self.canvas.create_text(x, y+12, text=self.weather_data.get("main", "--"),
                                font=("Consolas", 14, "bold"), fill=self.WHITE, anchor="w")
        self.canvas.create_text(x, y+32, text=self.weather_data.get("condition", "--"),
                                font=("Consolas", 8), fill=self.CYAN, anchor="w")
        self.canvas.create_text(x, y+45, text=self.weather_data.get("details", "--"),
                                font=("Consolas", 7), fill=self.CYAN_DIM, anchor="w")

    def _draw_agent_status(self):
        """Draw agent status indicator."""
        x, y = 60, 80
        colors = {"STANDBY": self.CYAN_DIM, "THINKING": self.PURPLE, "SEARCHING": self.ORANGE,
                  "OPENING": self.GREEN, "SPEAKING": self.GREEN, "LISTENING": self.CYAN}
        color = colors.get(self.agent_status, self.CYAN_DIM)

        self.canvas.create_rectangle(x-5, y-15, x+100, y+20, fill="#050a10", outline=color, width=1)
        self.canvas.create_text(x, y-5, text="AGENT", font=("Consolas", 7), fill=self.CYAN_DIM, anchor="w")

        # Pulsing dot
        dot_size = 4 + math.sin(self.time * 3) * 2 if self.agent_status != "STANDBY" else 3
        self.canvas.create_oval(x+80-dot_size, y+5-dot_size, x+80+dot_size, y+5+dot_size,
                                fill=color, outline="")
        self.canvas.create_text(x, y+8, text=self.agent_status, font=("Consolas", 8, "bold"),
                                fill=color, anchor="w")

    def _draw_hud(self):
        # Brackets
        self.canvas.create_line(20, 70, 20, 120, fill=self.CYAN_DIM, width=2)
        self.canvas.create_line(20, 70, 70, 70, fill=self.CYAN_DIM, width=2)
        self.canvas.create_line(680, 70, 680, 120, fill=self.CYAN_DIM, width=2)
        self.canvas.create_line(680, 70, 630, 70, fill=self.CYAN_DIM, width=2)
        self.canvas.create_line(20, 610, 20, 560, fill=self.CYAN_DIM, width=2)
        self.canvas.create_line(20, 610, 70, 610, fill=self.CYAN_DIM, width=2)
        self.canvas.create_line(680, 610, 680, 560, fill=self.CYAN_DIM, width=2)
        self.canvas.create_line(680, 610, 630, 610, fill=self.CYAN_DIM, width=2)

        # Top/bottom lines
        self.canvas.create_line(100, 60, 600, 60, fill=self.CYAN_DIM, width=1)
        self.canvas.create_line(100, 610, 600, 610, fill=self.CYAN_DIM, width=1)

        # Scan line
        scan_y = 60 + (self.time * 30) % 550
        self.canvas.create_line(100, scan_y, 600, scan_y, fill=self.CYAN_DIM, width=1)

    def _draw_particles(self):
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < 60:
                p["y"] = 610
                p["x"] = random.randint(50, 650)
            if p["x"] < 0 or p["x"] > 700:
                p["x"] = random.randint(50, 650)
            self.canvas.create_oval(p["x"]-p["size"], p["y"]-p["size"],
                                    p["x"]+p["size"], p["y"]+p["size"], fill=self.CYAN_DIM, outline="")

    def _draw_waveform(self, cx, cy):
        """Draw animated waveform bars."""
        num_bars = len(self.waveform_bars)
        bar_width = 6
        spacing = 2
        total_width = num_bars * (bar_width + spacing)
        start_x = cx - total_width // 2

        for i in range(num_bars):
            if self.state == "speaking":
                target = abs(math.sin(i * 0.4 + self.time * 8)) * 40 + 5
            elif self.state == "thinking":
                target = abs(math.sin(i * 0.3 + self.time * 4)) * 20 + 3
            else:
                target = 3

            self.waveform_bars[i] += (target - self.waveform_bars[i]) * 0.3

            x = start_x + i * (bar_width + spacing)
            h = self.waveform_bars[i]
            color = self.GREEN if self.state == "speaking" else self.PURPLE if self.state == "thinking" else self.CYAN_DIM

            self.canvas.create_rectangle(x, cy - h, x + bar_width, cy + h, fill=color, outline="")

    def _animate(self):
        self.time += 0.05
        self.pulse = math.sin(self.time * 2)

        self.canvas.delete("all")

        if self.state == "startup":
            self._draw_startup()
            if self.time > 5:
                self.state = "idle"
        else:
            self._draw_grid()
            self._draw_hud()
            self._draw_particles()
            self._draw_weather_dashboard()
            self._draw_agent_status()
            self._draw_arc_reactor(350, 330)
            self._draw_waveform(350, 520)

            # Title
            self.canvas.create_text(350, 25, text="S W A R A J", font=("Consolas", 11, "bold"), fill=self.CYAN_DIM)

            # Bottom panel
            self.canvas.create_text(350, 625, text="OUTPUT", font=("Consolas", 8), fill=self.CYAN_DIM)

        self.root.after(33, self._animate)

    def set_state(self, state):
        if self.state == "startup":
            return
        self.state = state

    def set_agent_status(self, status):
        self.agent_status = status.upper()

    def set_response(self, text):
        self.canvas.itemconfig(self.response_label, text=text)

    def _on_send(self, event):
        text = self.input_entry.get().strip()
        if text and self.on_send:
            self.input_entry.delete(0, "end")
            self.set_response(f"You: {text}")
            self.set_state("thinking")
            self.set_agent_status("THINKING")
            threading.Thread(target=self.on_send, args=(text,), daemon=True).start()

    def run(self):
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()


if __name__ == "__main__":
    ui = SwarajUI()
    ui.on_send = lambda t: ui.set_response(f"You said: {t}")
    ui.run()
