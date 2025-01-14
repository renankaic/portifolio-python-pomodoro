import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import math
import tkinter
import pygame


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 30
SHORT_BREAK_MIN = 10
LONG_BREAK_MIN = 30


# Função para buscar os arquivos no modo executável e no modo de desenvolvimento
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)


class PomodoroApp:
    def __init__(self) -> None:
        # ---------------------------- UI SETUP ------------------------------- #
        self.reps = 0
        self.timer = None
        self.is_paused = False
        self.last_count = 0

        self.window = tkinter.Tk()
        self.window.title("Pomodoro")
        self.window.config(bg=YELLOW, padx=20, pady=20)

        self.canvas = tkinter.Canvas(width=
                                     220, height=223,
                                     bg=YELLOW, highlightthickness=0)

        tomato_img = tkinter.PhotoImage(file=resource_path("./assets/img/tomato.png"))
        self.canvas.create_image(0, 0, image=tomato_img, anchor='nw')
        self.timer_txt = self.canvas.create_text(
            100, 130, fill="white", text="00:00", font=(FONT_NAME, 35, "bold"))
        self.canvas.grid(row=1, column=1, pady=20)

        self.lbl_title = tkinter.Label(text="Timer", fg=GREEN, font=(
            FONT_NAME, 42, "normal"), bg=YELLOW)
        self.lbl_title.grid(row=0, column=0, columnspan=3)

        self.lbl_check = tkinter.Label(fg=GREEN, bg=YELLOW)
        self.lbl_check.grid(row=3, column=1)

        icon_play = tkinter.PhotoImage(file=resource_path('./assets/icons/icon-play.png'))
        self.bt_start = tkinter.Button(
            text="Iniciar", highlightthickness=0, command=self.start_timer, width=100, pady=5, image=icon_play,
            compound='top')
        self.bt_start.grid(row=2, column=0)

        icon_pause = tkinter.PhotoImage(file=resource_path('./assets/icons/icon-pause.png'))
        self.bt_pause = tkinter.Button(text="Pausar", highlightthickness=0, command=self.pause_timer, width=100, pady=5,
                                       image=icon_pause, compound='top')
        self.bt_pause.grid(row=2, column=0)
        self.bt_pause.grid_remove()

        icon_reset = tkinter.PhotoImage(file=resource_path('./assets/icons/icon-reset.png'))
        bt_reset = tkinter.Button(
            text="Resetar", highlightthickness=0, command=self.reset_timer, width=100, pady=5, image=icon_reset,
            compound='top')
        bt_reset.grid(row=2, column=2)

        # Loads notify sound
        pygame.mixer.init()
        pygame.mixer.music.load(resource_path('./assets/sounds/sound.wav'))

        self.window.mainloop()

    # ---------------------------- TIMER MECHANISM ------------------------------- #
    def start_timer(self):
        self.reps += 1

        if self.reps % 8 == 0:
            next_count = LONG_BREAK_MIN * 60 if not self.is_paused else self.last_count
            self.lbl_title.config(text="Pausa Longa", fg=RED)
        elif self.reps % 2 == 0:
            next_count = SHORT_BREAK_MIN * 60 if not self.is_paused else self.last_count
            self.lbl_title.config(text="Pausa", fg=PINK)
            self.lbl_check.config(text=self.lbl_check.cget("text") + "✔")
        else:
            next_count = WORK_MIN * 60 if not self.is_paused else self.last_count
            self.lbl_title.config(text="Foque!", fg=GREEN)

        self.play_alarm_sound()
        self.window.focus_force()
        self.count_down(next_count)
        self.bt_start.grid_remove()
        self.bt_pause.grid()

    def pause_timer(self):
        self.window.after_cancel(self.timer)
        self.reps -= 1
        self.bt_pause.grid_remove()
        self.bt_start.grid()
        self.is_paused = True
        self.lbl_title.config(text='Pausado!', fg=GREEN)

    # ---------------------------- TIMER RESET ------------------------------- #
    def reset_timer(self):
        self.lbl_title.config(text="Timer", fg=GREEN)
        self.lbl_check.config(text="")
        self.canvas.itemconfig(self.timer_txt, text="00:00")
        self.window.after_cancel(self.timer)
        self.is_paused = False
        self.last_count = 0
        self.reps = 0

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

    def count_down(self, count):
        self.last_count = count
        count_minutes = math.floor(count / 60)
        count_seconds = count % 60

        if count_seconds < 10:
            count_seconds = f"0{count_seconds}"

        self.canvas.itemconfig(
            self.timer_txt, text=f"{count_minutes}:{count_seconds}")
        if count > 0:
            if self.timer:
                self.window.after_cancel(self.timer)
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.last_count = count
            self.start_timer()

    @staticmethod
    def play_alarm_sound():
        pygame.mixer.music.play()


if __name__ == "__main__":
    app = PomodoroApp()
