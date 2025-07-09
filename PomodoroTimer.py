#Author: Niranjan Apte
#Date: 8th July 2025
import tkinter as tk
import time
import threading
import random
from tkinter import messagebox
import winsound

# ---------------- CONFIG ---------------- #
WORK_MIN = 25
BREAK_MIN = 5
LONG_BREAK_MIN = 15
SESSIONS_BEFORE_LONG_BREAK = 4

EXERCISES = [
    "Do 10 push-ups 💪",
    "Do 20 squats 🏋️",
    "Practice deep breathing for 1 minute 🧘",
    "Try alternate nostril breathing (Nadi Shodhana) 🧘‍♂️",
    "Stretch arms and shoulders 🙆",
    "Take a short walk 🏃‍♂️",
    "Hydrate – drink a glass of water 💧"
]

# -------------- TIMER LOGIC -------------- #
class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.session_count = 0
        self.running = False

        self.label = tk.Label(root, text="Ready to focus?", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.timer_display = tk.Label(root, text="25:00", font=("Helvetica", 36))
        self.timer_display.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(pady=5)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.session_count += 1
            session_type = "Work" if self.session_count % 2 != 0 else "Break"
            duration = WORK_MIN if session_type == "Work" else (
                LONG_BREAK_MIN if self.session_count % (SESSIONS_BEFORE_LONG_BREAK * 2) == 0 else BREAK_MIN
            )
            self.label.config(text=f"{session_type} session")
            threading.Thread(target=self.countdown, args=(duration * 60, session_type), daemon=True).start()

    def countdown(self, count, session_type):
        while count > 0 and self.running:
            mins, secs = divmod(count, 60)
            self.timer_display.config(text=f"{mins:02}:{secs:02}")
            self.root.update()
            time.sleep(1)
            count -= 1
        if self.running:
            if session_type == "Break":
                reminder = random.choice(EXERCISES)
                winsound.MessageBeep()  # 🔔 Triggers system notification sound
                messagebox.showinfo("Break Reminder", f"Time for a quick break:\n\n{reminder}")
            self.running = False
            self.start_timer()

    def reset_timer(self):
        self.running = False
        self.session_count = 0
        self.label.config(text="Timer reset. Ready?")
        self.timer_display.config(text="25:00")

# -------------- RUN APP -------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
