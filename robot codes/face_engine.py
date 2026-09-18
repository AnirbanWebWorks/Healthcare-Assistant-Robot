import tkinter as tk
import time
import random

class FaceEngine:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(True)   # 🔥 removes title bar + taskbar
        self.root.config(cursor="none")    # 🔥 hide mouse
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # ✅ Display size
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        self.root.geometry(f"{self.w}x{self.h}+0+0")
        self.color = "#1E9ACB"
        self.expression = "idle"

        self.draw_idle()

        # 🔥 Start animation loop (Tkinter-safe)
        self.animate()

    # 🔵 ROUNDED RECT
    def rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        return self.canvas.create_polygon(
            x1+r, y1, x2-r, y1,
            x2, y1+r, x2, y2-r,
            x2-r, y2, x1+r, y2,
            x1, y2-r, x1, y1+r,
            smooth=True, **kwargs
        )

    # 👁️ EYES
    def draw_eyes(self, tilt=0, shrink=0):
        lx, rx = self.w*0.3, self.w*0.7
        y = self.h*0.35

        sx = self.w * 0.12 - shrink
        sy = self.h * 0.18 - shrink

        self.rounded_rect(lx-sx, y-sy+tilt, lx+sx, y+sy+tilt, 30, fill=self.color)
        self.rounded_rect(rx-sx, y-sy-tilt, rx+sx, y+sy-tilt, 30, fill=self.color)

    # 🙂 MOUTH
    def draw_mouth(self, mood):
        mx = self.w * 0.5
        my = self.h * 0.7
        w = self.w * 0.12

        if mood == "happy":
            points = [mx-w, my, mx, my+20, mx+w, my]
        elif mood == "sad":
            points = [mx-w, my+20, mx, my-20, mx+w, my+20]
        else:
            points = [mx-w, my, mx, my+5, mx+w, my]

        self.canvas.create_line(points, fill=self.color, width=4, smooth=True)

    # 😐 IDLE
    def draw_idle(self):
        self.canvas.delete("all")
        self.draw_eyes()
        self.draw_mouth("neutral")

    # 😄 SMILE
    def draw_smile(self):
        self.canvas.delete("all")
        self.draw_eyes(shrink=5)
        self.draw_mouth("happy")

    # 🗣️ TALK
    def draw_talk(self, openness=10):
        self.canvas.delete("all")
        self.draw_eyes()

        mx = self.w * 0.5
        my = self.h * 0.7
        width = self.w * 0.12

        # 🔥 Semi-circle arc (mouth)
        self.canvas.create_arc(
            mx - width,
            my - openness,
            mx + width,
            my + openness,
            start=200, extent=140,   # semi-circle shape
            style="arc",
            outline=self.color,
            width=5
        )

    # 👁️ BLINK
    def blink(self):
        self.canvas.delete("all")

        lx, rx = self.w*0.3, self.w*0.7
        y = self.h*0.35

        self.canvas.create_line(lx-80, y, lx+80, y, fill=self.color, width=8)
        self.canvas.create_line(rx-80, y, rx+80, y, fill=self.color, width=8)

        self.root.after(120, self.draw_idle)

    # 🔁 ANIMATION LOOP (SAFE)
    def animate(self):
        if self.expression == "idle":
            if random.random() < 0.05:
                self.blink()

        elif self.expression == "talk":
            for open_level in [5, 15, 8, 18]:
                self.draw_talk(openness=open_level)
                self.root.update()
                time.sleep(0.08)

        elif self.expression == "smile":
            self.draw_smile()

        # 🔁 loop safely
        self.root.after(150, self.animate)

    # ✅ CORRECT METHOD
    def set_expression(self, expr):
        self.expression = expr


# 🔥 GLOBAL INSTANCE
face = FaceEngine()

# 🚀 START UI (MAIN THREAD)
def start_face():
    face.root.mainloop()

# 🔥 THREAD-SAFE EXPRESSION CONTROL
def set_expression(expr):
    def update():
        face.set_expression(expr)

    try:
        face.root.after(0, update)
    except:
        pass