"""
Swaraj UI - Jarvis-Grade Interface with Rajmudra
=================================================
Shows Rajmudra on startup, then transitions to arc reactor.
"""

import tkinter as tk
from tkinter import ttk
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

        # State
        self.state = "startup"
        self.time = 0
        self.pulse = 0
        self.startup_alpha = 0
        self.startup_stage = 0
        self.particles = []

        # Load Rajmudra image
        self.rajmudra_img = None
        self._load_rajmudra()

        self._setup_ui()
        self._init_particles()
        self._animate()

    def _load_rajmudra(self):
        """Load the Rajmudra image."""
        img_path = os.path.join(os.path.dirname(__file__), "assets", "rajmudra.png")
        if os.path.exists(img_path):
            try:
                from PIL import Image, ImageTk
                self.rajmudra_img = Image.open(img_path)
                self.rajmudra_img = self.rajmudra_img.resize((300, 300), Image.Resampling.LANCZOS)
                self.rajmudra_photo = ImageTk.PhotoImage(self.rajmudra_img)
                self.has_image = True
            except ImportError:
                print("Pillow not installed. Install with: pip install Pillow")
                self.has_image = False
            except Exception as e:
                print(f"Error loading image: {e}")
                self.has_image = False
        else:
            print(f"Image not found at: {img_path}")
            print("Please save your Rajmudra image to: assets/rajmudra.png")
            self.has_image = False

    def _setup_ui(self):
        self.canvas = tk.Canvas(
            self.root, width=700, height=750,
            bg=self.DARK, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.status_text = self.canvas.create_text(
            350, 720, text="",
            font=("Consolas", 9),
            fill=self.GREEN
        )

        # Response area
        self.canvas.create_rectangle(
            50, 620, 650, 710,
            fill="#050a10", outline=self.CYAN_DIM, width=1
        )
        self.response_label = self.canvas.create_text(
            350, 665, text="",
            font=("Consolas", 10),
            fill=self.WHITE,
            width=580
        )

        # Input
        self.input_frame = tk.Frame(self.root, bg="#050a10")
        self.input_frame.place(x=60, y=715, width=480, height=30)

        self.input_entry = tk.Entry(
            self.input_frame,
            font=("Consolas", 10),
            bg="#0a1020",
            fg=self.CYAN,
            insertbackground=self.CYAN,
            relief="flat"
        )
        self.input_entry.pack(fill="both", expand=True, padx=2, pady=2)
        self.input_entry.bind("<Return>", self._on_send)

        self.send_btn = tk.Canvas(
            self.root, width=80, height=30,
            bg="#0a1020", highlightthickness=0, cursor="hand2"
        )
        self.send_btn.place(x=550, y=717)
        self.send_btn.create_text(40, 15, text="SEND", font=("Consolas", 9, "bold"), fill=self.CYAN)
        self.send_btn.bind("<Button-1>", lambda e: self._on_send(None))

        self.on_send = None

    def _init_particles(self):
        for _ in range(40):
            self.particles.append({
                "x": random.randint(50, 650),
                "y": random.randint(80, 600),
                "vx": random.uniform(-0.2, 0.2),
                "vy": random.uniform(-0.3, 0.1),
                "size": random.uniform(0.5, 1.5),
                "alpha": random.randint(30, 70)
            })

    def _draw_grid(self):
        for x in range(0, 700, 40):
            self.canvas.create_line(x, 60, x, 610, fill="#060d15", width=1)
        for y in range(60, 610, 40):
            self.canvas.create_line(0, y, 700, y, fill="#060d15", width=1)

    def _draw_startup(self):
        """Draw the Rajmudra startup sequence."""
        cx, cy = 350, 320
        t = self.time

        # Background fade in
        self.startup_alpha = min(1.0, self.startup_alpha + 0.02)

        # Draw Rajmudra image if available
        if self.has_image:
            # Pulsing glow behind image
            glow_size = 180 + math.sin(t * 2) * 10
            for i in range(5, 0, -1):
                r = glow_size + i * 8
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    outline=self.GOLD, width=1
                )

            # Draw the image
            self.canvas.create_image(cx, cy, image=self.rajmudra_photo)

            # Rotating rings around the image
            for ring in range(3):
                r = 170 + ring * 15
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
            # Fallback - draw a placeholder
            self.canvas.create_text(
                cx, cy, text="RAJMUDRA",
                font=("Consolas", 24, "bold"),
                fill=self.GOLD
            )
            self.canvas.create_text(
                cx, cy + 40, text="[Place rajmudra.png in assets/]",
                font=("Consolas", 10),
                fill=self.CYAN_DIM
            )

        # Title
        self.canvas.create_text(
            cx, 550, text="S W A R A J",
            font=("Consolas", 16, "bold"),
            fill=self.GOLD
        )
        self.canvas.create_text(
            cx, 575, text="चत्रपती शिवाजी महाराजांच्या आदर्शावर",
            font=("Consolas", 10),
            fill=self.CYAN_DIM
        )

        # Loading bar
        progress = min(1.0, (t - 1) / 4)  # 4 second startup
        bar_width = 300
        bar_x = cx - bar_width // 2
        bar_y = 600

        self.canvas.create_rectangle(
            bar_x, bar_y, bar_x + bar_width, bar_y + 8,
            outline=self.CYAN_DIM, width=1
        )
        self.canvas.create_rectangle(
            bar_x, bar_y, bar_x + bar_width * progress, bar_y + 8,
            fill=self.CYAN, outline=""
        )

        if progress >= 1.0:
            self.canvas.create_text(
                cx, 615, text="SYSTEMS ONLINE",
                font=("Consolas", 9),
                fill=self.GREEN
            )

    def _draw_arc_reactor(self, cx, cy):
        """Draw the main arc reactor."""
        t = self.time
        state_colors = {
            "idle": self.CYAN_DIM,
            "listening": self.CYAN,
            "thinking": self.PURPLE,
            "speaking": self.GREEN
        }
        glow_color = state_colors.get(self.state, self.CYAN_DIM)

        # Outer glow
        for i in range(15, 0, -1):
            r = 80 + i * 4 + self.pulse * 3
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=glow_color, width=1)

        # Ring 1
        r1 = 100
        for i in range(24):
            angle = (i / 24) * 2 * math.pi + t * 0.5
            x1 = cx + r1 * math.cos(angle)
            y1 = cy + r1 * math.sin(angle)
            x2 = cx + r1 * math.cos(angle + 0.3)
            y2 = cy + r1 * math.sin(angle + 0.3)
            if i % 2 == 0:
                self.canvas.create_line(x1, y1, x2, y2, fill=self.CYAN, width=2)

        # Ring 2
        r2 = 75
        for i in range(16):
            angle = (i / 16) * 2 * math.pi - t * 0.8
            x1 = cx + r2 * math.cos(angle)
            y1 = cy + r2 * math.sin(angle)
            x2 = cx + r2 * math.cos(angle + 0.25)
            y2 = cy + r2 * math.sin(angle + 0.25)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.BLUE, width=2)

        # Ring 3
        r3 = 50
        for i in range(12):
            angle = (i / 12) * 2 * math.pi + t * 1.2
            x1 = cx + r3 * math.cos(angle)
            y1 = cy + r3 * math.sin(angle)
            x2 = cx + r3 * math.cos(angle + 0.4)
            y2 = cy + r3 * math.sin(angle + 0.4)
            color = self.PURPLE if self.state == "thinking" else self.CYAN
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        # Core
        core_size = 20 + self.pulse * 5
        core_colors = {"idle": self.CYAN, "listening": "#00ffff",
                       "thinking": "#aa44ff", "speaking": "#00ff88"}
        self.canvas.create_oval(
            cx - core_size, cy - core_size,
            cx + core_size, cy + core_size,
            fill=core_colors.get(self.state, self.CYAN),
            outline=self.WHITE, width=1
        )
        inner = core_size * 0.5
        self.canvas.create_oval(cx-inner, cy-inner, cx+inner, cy+inner, fill="#ffffff", outline="")

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

        # Lines
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
            self.canvas.create_oval(
                p["x"]-p["size"], p["y"]-p["size"],
                p["x"]+p["size"], p["y"]+p["size"],
                fill=self.CYAN_DIM, outline=""
            )

    def _draw_waveform(self, cx, cy):
        if self.state != "speaking":
            return
        for i in range(100):
            x = cx - 120 + i * 2.4
            amp = math.sin(i * 0.3 + self.time * 5) * 15 * math.sin(i * 0.1)
            y = cy + amp
            if i > 0:
                self.canvas.create_line(prev_x, prev_y, x, y, fill=self.GREEN, width=2)
            prev_x, prev_y = x, y

    def _animate(self):
        self.time += 0.05
        self.pulse = math.sin(self.time * 2)

        self.canvas.delete("all")

        if self.state == "startup":
            self._draw_startup()
            # Auto transition after 5 seconds
            if self.time > 5:
                self.state = "idle"
        else:
            self._draw_grid()
            self._draw_hud()
            self._draw_particles()
            self._draw_arc_reactor(350, 330)
            self._draw_waveform(350, 500)

            # Title
            self.canvas.create_text(350, 25, text="S W A R A J",
                                    font=("Consolas", 11, "bold"), fill=self.CYAN_DIM)

            # Status
            state_labels = {
                "idle": ("STANDBY", self.CYAN_DIM),
                "listening": ("LISTENING", self.CYAN),
                "thinking": ("PROCESSING", self.PURPLE),
                "speaking": ("SPEAKING", self.GREEN)
            }
            label, color = state_labels.get(self.state, ("STANDBY", self.CYAN_DIM))
            self.canvas.itemconfig(self.status_text, text=label, fill=color)

            # Bottom panel
            self.canvas.create_text(350, 625, text="OUTPUT",
                                    font=("Consolas", 8), fill=self.CYAN_DIM)

        self.root.after(33, self._animate)

    def set_state(self, state):
        if self.state == "startup":
            return
        self.state = state

    def set_response(self, text):
        self.canvas.itemconfig(self.response_label, text=text)

    def _on_send(self, event):
        text = self.input_entry.get().strip()
        if text and self.on_send:
            self.input_entry.delete(0, "end")
            self.set_response(f"You: {text}")
            self.set_state("thinking")
            threading.Thread(target=self.on_send, args=(text,), daemon=True).start()

    def run(self):
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()


if __name__ == "__main__":
    ui = SwarajUI()
    ui.on_send = lambda t: ui.set_response(f"You said: {t}")
    ui.run()
