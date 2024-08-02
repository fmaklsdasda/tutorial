import tkinter as tk
import time
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game

class MovingGame(tk.Frame):
    def __init__(self, game: "Game"):
        super().__init__(game.container)
        self.game = game
        self.game.title("Moving Object Game")
        width = game.container.winfo_width()
        height = game.container.winfo_height()

        self.canvas_width = width
        self.canvas_height = height//2
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.rect = self.canvas.create_rectangle(20, 80, 40, 100, fill="blue")

        self.update_target_position()

        self.moving_speed = 10
        self.direction = 1
        self.start_time = time.time()
        self.game.bind("<s>", self.check_hit)
        self.total_score = 0
        self.score_text = self.canvas.create_text(self.canvas_width // 2, self.canvas_height - 20, text=f"Score: {self.total_score}", font=("Arial", 16))

        self.move_object()

        tk.Button(self, text="В меню", command=self.game.open_menu).pack()

    def unmount(self):
        self.game.unbind("<s>")
        


    def move_object(self):
        self.canvas.move(self.rect, self.direction * self.moving_speed, 0)
        pos = self.canvas.coords(self.rect)
        if pos[2] >= self.canvas_width or pos[0] <= 0:
            self.direction *= -1
        self.game.after(50, self.move_object)

    def check_hit(self, event):
        pos = self.canvas.coords(self.rect)
        if self.target_position - 10 <= pos[0] <= self.target_position + 10:
            score = max(100 - abs(self.target_position - pos[0]), 0)
            self.total_score += score
        self.update_target_position()
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.total_score}")

    def update_target_position(self):
        self.target_position = random.randint(100, self.canvas_width - 100)
        if hasattr(self, 'target_line'):
            self.canvas.coords(self.target_line, self.target_position, 50, self.target_position, 150)
        else:
            self.target_line = self.canvas.create_line(self.target_position, 50, self.target_position, 150, fill="red")
