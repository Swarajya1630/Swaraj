"""
Expanded Assistant Window
========================
Full JARVIS interface with conversation, controls, and system status.
Opens when clicking the compact widget.
"""

import tkinter as tk
import math
import time
import threading


class ExpandedWindow:
    def __init__(self, app=None):
        self.app = app
        self.root = None
        self.canvas = None
        self._running = False
        self._visible = False

        self.state = "idle"
        self.time = 0
        self.pulse = 0
        self.conversation = []
        self.waveform_bars = [0] * 32
        self.status_text = "STANDBY"
        self.system_status = {"cpu": 0, "ram": 0, "disk": 0}

        self.CYAN = "#00d4ff"
        self.CYAN_DIM = "#004466"
        self.BLUE = "#0066cc"
        self.GREEN = "#00ff88"
        self.PURPLE = "#8800ff"
        self.ORANGE = "#ff8800"
        self.WHITE = "#ffffff"
        self.DARK = "#0a0a12"
        self.GOLD = "#c9a227"

    def show(self):
        if self._visible and self.root:
            self.root.lift()
            return

        self._visible = True
        self.root = tk.Tk()
        self.root.title("SWARAJ - AI Assistant")
        self.root.geometry("700x800")
        self.root.configure(bg=self.DARK)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        screen_w = self.root.winfo_screenwidth()
        x = (screen_w - 700) // 2
        y = 50
        self.root.geometry(f"700x800+{x}+{y}")

        self.canvas = tk.Canvas(
            self.root, width=700, height=800,
            bg=self.DARK, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self._setup_ui()
        self._animate()

    def _setup_ui(self):
        self.canvas.create_rectangle(10, 10, 690, 790, outline=self.CYAN_DIM, width=1, fill=self.DARK)

        self.canvas.create_text(350, 30, text="S W A R A J", font=("Consolas", 14, "bold"), fill=self.CYAN)
        self.canvas.create_text(350, 50, text="AI ASSISTANT", font=("Consolas", 9), fill=self.CYAN_DIM)

        self.canvas.create_line(20, 65, 680, 65, fill=self.CYAN_DIM, width=1)

        self.canvas.create_text(30, 80, text="STATUS", font=("Consolas", 8), fill=self.CYAN_DIM, anchor="w")
        self.status_label = self.canvas.create_text(100, 80, text="STANDBY", font=("Consolas", 8, "bold"),
                                                     fill=self.CYAN, anchor="w")

        self.canvas.create_text(500, 80, text="CPU", font=("Consolas", 7), fill=self.CYAN_DIM, anchor="w")
        self.cpu_bar = self.canvas.create_rectangle(540, 76, 600, 84, outline=self.CYAN_DIM, width=1)
        self.cpu_fill = self.canvas.create_rectangle(540, 76, 540, 84, fill=self.CYAN, outline="")

        self.canvas.create_text(500, 95, text="RAM", font=("Consolas", 7), fill=self.CYAN_DIM, anchor="w")
        self.ram_bar = self.canvas.create_rectangle(540, 91, 600, 99, outline=self.CYAN_DIM, width=1)
        self.ram_fill = self.canvas.create_rectangle(540, 91, 540, 99, fill=self.GREEN, outline="")

        self.conv_frame = tk.Frame(self.root, bg=self.DARK)
        self.conv_frame.place(x=20, y=105, width=660, height=500)

        self.conv_canvas = tk.Canvas(self.conv_frame, bg="#050a10", highlightthickness=0)
        self.conv_scrollbar = tk.Scrollbar(self.conv_frame, orient="vertical", command=self.conv_canvas.yview)
        self.conv_inner = tk.Frame(self.conv_canvas, bg="#050a10")

        self.conv_inner.bind("<Configure>", lambda e: self.conv_canvas.configure(scrollregion=self.conv_canvas.bbox("all")))
        self.conv_canvas.create_window((0, 0), window=self.conv_inner, anchor="nw")
        self.conv_canvas.configure(yscrollcommand=self.conv_scrollbar.set)

        self.conv_scrollbar.pack(side="right", fill="y")
        self.conv_canvas.pack(side="left", fill="both", expand=True)

        self.canvas.create_line(20, 615, 680, 615, fill=self.CYAN_DIM, width=1)

        self.canvas.create_text(350, 630, text="WAVEFORM", font=("Consolas", 7), fill=self.CYAN_DIM)

        self.input_frame = tk.Frame(self.root, bg="#0a1020")
        self.input_frame.place(x=20, y=720, width=560, height=35)

        self.input_entry = tk.Entry(
            self.input_frame, font=("Consolas", 11), bg="#0a1020",
            fg=self.CYAN, insertbackground=self.CYAN, relief="flat"
        )
        self.input_entry.pack(fill="both", expand=True, padx=5, pady=5)
        self.input_entry.bind("<Return>", self._on_send)

        self.send_btn = tk.Canvas(self.root, width=100, height=35, bg="#0a1020",
                                   highlightthickness=0, cursor="hand2")
        self.send_btn.place(x=590, y=720)
        self.send_btn.create_text(50, 17, text="SEND", font=("Consolas", 10, "bold"), fill=self.CYAN)
        self.send_btn.bind("<Button-1>", lambda e: self._on_send(None))

        self.mic_btn = tk.Canvas(self.root, width=50, height=35, bg="#0a1020",
                                  highlightthickness=0, cursor="hand2")
        self.mic_btn.place(x=640, y=720)
        self.mic_btn.create_text(25, 17, text="MIC", font=("Consolas", 9, "bold"), fill=self.GREEN)

        self.response_text = self.canvas.create_text(
            350, 680, text="", font=("Consolas", 10), fill=self.WHITE, width=650
        )

        self.on_send = None

    def _on_send(self, event):
        text = self.input_entry.get().strip()
        if text:
            self.input_entry.delete(0, "end")
            self.add_message("You", text)
            self.set_state("thinking")
            if self.on_send:
                threading.Thread(target=self.on_send, args=(text,), daemon=True).start()

    def add_message(self, sender, text):
        if not self.conv_inner:
            return

        is_user = sender == "You"
        bg = "#0a1525" if is_user else "#050a10"
        fg = self.CYAN if is_user else self.WHITE
        anchor = "e" if is_user else "w"

        msg_frame = tk.Frame(self.conv_inner, bg=bg)
        msg_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(msg_frame, text=sender, font=("Consolas", 8, "bold"),
                 fg=self.CYAN_DIM if is_user else self.GREEN, bg=bg).pack(anchor=anchor)
        tk.Label(msg_frame, text=text, font=("Consolas", 10), fg=fg, bg=bg,
                 wraplength=600, justify="left").pack(anchor=anchor)

        self.conversation.append({"sender": sender, "text": text})
        self.conv_canvas.update_idletasks()
        self.conv_canvas.yview_moveto(1.0)

    def _draw_waveform(self, cx, cy):
        num_bars = len(self.waveform_bars)
        bar_width = 5
        spacing = 2
        total_width = num_bars * (bar_width + spacing)
        start_x = cx - total_width // 2

        for i in range(num_bars):
            if self.state == "speaking":
                target = abs(math.sin(i * 0.4 + self.time * 8)) * 20 + 3
            elif self.state == "thinking":
                target = abs(math.sin(i * 0.3 + self.time * 4)) * 12 + 3
            elif self.state == "listening":
                target = abs(math.sin(i * 0.3 + self.time * 5)) * 8 + 3
            else:
                target = 3

            self.waveform_bars[i] += (target - self.waveform_bars[i]) * 0.3

            x = start_x + i * (bar_width + spacing)
            h = self.waveform_bars[i]
            color = self.GREEN if self.state == "speaking" else \
                   self.PURPLE if self.state == "thinking" else self.CYAN_DIM

            self.canvas.create_rectangle(x, cy - h, x + bar_width, cy + h, fill=color, outline="")

    def _update_status(self):
        if not self.canvas:
            return

        state_colors = {
            "idle": self.CYAN_DIM,
            "listening": self.CYAN,
            "thinking": self.PURPLE,
            "speaking": self.GREEN
        }
        color = state_colors.get(self.state, self.CYAN_DIM)

        self.canvas.itemconfig(self.status_label, text=self.status_text, fill=color)

    def _animate(self):
        if not self._running and not self._visible:
            return

        self.time += 0.05
        self.pulse = math.sin(self.time * 2)

        if self.canvas:
            self.canvas.delete("waveform")
            self._draw_waveform()
            self._update_status()

        if self.root and self._visible:
            self.root.after(50, self._animate)

    def set_state(self, state):
        self.state = state

    def set_status(self, text):
        self.status_text = text

    def set_response(self, text):
        if self.canvas:
            self.canvas.itemconfig(self.response_text, text=text)

    def hide(self):
        self._visible = False
        if self.root:
            self.root.withdraw()

    def show_window(self):
        if self.root:
            self._visible = True
            self.root.deiconify()
            self.root.lift()

    def stop(self):
        self._running = False
        self._visible = False
        if self.root:
            self.root.after(100, self.root.destroy)
