"""
Animation Utilities
==================
Shared animation helpers for Swaraj UI components.
"""

import math
import random


class AnimationHelper:
    def __init__(self):
        self.time = 0
        self.pulse = 0
        self.particles = []

    def update(self, dt=0.05):
        self.time += dt
        self.pulse = math.sin(self.time * 2)

    def get_pulse(self, speed=2, amplitude=1):
        return math.sin(self.time * speed) * amplitude

    def get_breathe(self, min_val=0.8, max_val=1.2, speed=1.5):
        t = (math.sin(self.time * speed) + 1) / 2
        return min_val + t * (max_val - min_val)

    def init_particles(self, count=30, bounds=(0, 0, 700, 600)):
        self.particles = []
        x_min, y_min, x_max, y_max = bounds
        for _ in range(count):
            self.particles.append({
                "x": random.randint(x_min, x_max),
                "y": random.randint(y_min, y_max),
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-0.4, 0.1),
                "size": random.uniform(0.5, 2.0),
                "alpha": random.uniform(0.3, 0.8)
            })

    def update_particles(self, bounds=(0, 0, 700, 600)):
        x_min, y_min, x_max, y_max = bounds
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < y_min:
                p["y"] = y_max
                p["x"] = random.randint(x_min, x_max)
            if p["x"] < x_min or p["x"] > x_max:
                p["x"] = random.randint(x_min, x_max)

    def draw_arc_ring(self, canvas, cx, cy, radius, segments=24, speed=0.5, color="#003d55", width=1):
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi + self.time * speed
            x1 = cx + radius * math.cos(angle)
            y1 = cy + radius * math.sin(angle)
            x2 = cx + radius * math.cos(angle + 0.2)
            y2 = cy + radius * math.sin(angle + 0.2)
            canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    def draw_waveform(self, canvas, cx, cy, num_bars=24, bar_width=4, spacing=2,
                       state="idle", color="#003d55"):
        total_width = num_bars * (bar_width + spacing)
        start_x = cx - total_width // 2

        for i in range(num_bars):
            if state == "speaking":
                target = abs(math.sin(i * 0.5 + self.time * 8)) * 15 + 2
            elif state == "thinking":
                target = abs(math.sin(i * 0.4 + self.time * 4)) * 8 + 2
            elif state == "listening":
                target = abs(math.sin(i * 0.3 + self.time * 5)) * 6 + 2
            else:
                target = 2

            x = start_x + i * (bar_width + spacing)
            h = target

            bar_color = "#00ff88" if state == "speaking" else \
                       "#8800ff" if state == "thinking" else \
                       "#00d4ff" if state == "listening" else color

            canvas.create_rectangle(x, cy - h, x + bar_width, cy + h,
                                    fill=bar_color, outline="")

    def draw_glow(self, canvas, cx, cy, radius, color="#00d4ff", layers=5):
        for i in range(layers, 0, -1):
            r = radius + i * 4
            alpha = 0.3 * (1 - i / layers)
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=1)
