import math
import tkinter

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 2
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 4

reps = 0
timer = None


class PomodoroApp:
    def __init__(self) -> None:
        # ---------------------------- UI SETUP ------------------------------- #
        self.window = tkinter.Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)

        self.canvas = tkinter.Canvas(width=200, height=224,
                                     bg=YELLOW, highlightthickness=0)
        tomato_img = tkinter.PhotoImage(file="tomato.png")
        self.canvas.create_image(100, 112, image=tomato_img)
        self.timer_txt = self.canvas.create_text(
            100, 130, fill="white", text="00:00", font=(FONT_NAME, 35, "bold"))
        self.canvas.grid(row=1, column=1, padx=20, pady=20)

        self.lbl_title = tkinter.Label(text="Timer", fg=GREEN, font=(
            FONT_NAME, 42, "normal"), bg=YELLOW)
        self.lbl_title.grid(row=0, column=1)

        self.lbl_check = tkinter.Label(fg=GREEN, bg=YELLOW)
        self.lbl_check.grid(row=3, column=1)

        bt_start = tkinter.Button(
            text="Start", highlightthickness=0, command=self.start_timer)
        bt_start.grid(row=2, column=0)

        bt_reset = tkinter.Button(
            text="Reset", highlightthickness=0, command=self.reset_timer)
        bt_reset.grid(row=2, column=2)

        self.window.mainloop()

    # ---------------------------- TIMER MECHANISM ------------------------------- #
    def start_timer(self):
        global reps
        reps += 1

        if reps % 8 == 0:
            self.count_down(LONG_BREAK_MIN * 60)
            self.lbl_title.config(text="Break", fg=RED)
        elif reps % 2 == 0:
            self.count_down(SHORT_BREAK_MIN * 60)
            self.lbl_title.config(text="Break", fg=PINK)
            self.lbl_check.config(text=self.lbl_check.cget("text") + "✔")
        else:
            self.count_down(WORK_MIN * 60)
            self.lbl_title.config(text="Work", fg=GREEN)

    # ---------------------------- TIMER RESET ------------------------------- #
    def reset_timer(self):
        self.lbl_title.config(text="Timer", fg=GREEN)
        self.lbl_check.config(text="")
        self.canvas.itemconfig(self.timer_txt, text="00:00")
        self.window.after_cancel(timer)

        global reps
        reps = 0

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

    def count_down(self, count):
        count_minutes = math.floor(count / 60)
        count_seconds = count % 60

        if count_seconds < 10:
            count_seconds = f"0{count_seconds}"

        self.canvas.itemconfig(
            self.timer_txt, text=f"{count_minutes}:{count_seconds}")
        if count > 0:
            global timer
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.start_timer()


if __name__ == "__main__":
    app = PomodoroApp()
