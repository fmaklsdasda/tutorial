import tkinter as tk
import time
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game


class Turn: 
    def __init__(self, angle, distance):
        self.angle = angle 
        self.distance = distance

track = [Turn(30, 1020), Turn(60, 200), Turn(178, 400)]
    

class MovingGame(tk.Frame):

    car_width = 20

    def __init__(self, game: "Game"):
        super().__init__(game.container)
        self.game = game
        self.game.title("Moving Object Game")
        width = game.container.winfo_width()
        height = game.container.winfo_height()

        self.canvas_width = width
        self.canvas_height = height // 2
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.rect = self.canvas.create_rectangle(self.car_width, 80, 40, 100, fill="blue")

        self.minimap_width = width
        self.minimap_height = 50
        self.minimap_canvas = tk.Canvas(self, width=self.minimap_width, height=self.minimap_height)
        self.minimap_canvas.pack()

        self.track_line = self.minimap_canvas.create_line(10, self.minimap_height // 2, self.minimap_width - 10, self.minimap_height // 2, fill="black", width=2)
        self.track_length = len(track)
        self.minimap_positions = self.create_minimap_markers()

        self.current_turn_index = 0
        self.update_minimap(self.current_turn_index)

        self.update_target_position()

        self.moving_speed = 10
        self.direction = 1
        self.start_time = time.time()
        self.game.bind("<s>", self.check_hit)
        self.total_score = 0
        self.score_text = self.canvas.create_text(self.canvas_width // 2, self.canvas_height - 20, text=f"Score: {self.total_score}", font=("Arial", 16))

        self.move_object()

        tk.Button(self, text="В меню", command=self.game.open_menu).pack()

    def create_minimap_markers(self):
        markers = []
        current_position = 10
        for i in range(self.track_length):
            current_position += (self.minimap_width - 20) / self.track_length
            marker = self.minimap_canvas.create_line(current_position, 0, current_position, self.minimap_height, fill="red", dash=(3, 5)) # figure out how it works
            markers.append(current_position)
        return markers

    def update_minimap(self, turn_index):
        # Update the marker's position based on the current turn index
        position_on_minimap = self.minimap_positions[turn_index]
        if hasattr(self, 'minimap_rect'):
            self.minimap_canvas.coords(self.minimap_rect, position_on_minimap - 5, self.minimap_height // 2 - 5, position_on_minimap + 5, self.minimap_height // 2 + 5)
        else:
            self.minimap_rect = self.minimap_canvas.create_rectangle(position_on_minimap - 5, self.minimap_height // 2 - 5, position_on_minimap + 5, self.minimap_height // 2 + 5, fill="blue")

    def unmount(self):
        self.game.unbind("<s")

    def move_object(self):
        self.canvas.move(self.rect, self.direction * self.moving_speed, 0)
        pos = self.canvas.coords(self.rect)
        if pos[2] >= self.canvas_width or pos[0] <= 0:
            self.direction *= -1
            self.current_turn_index = (self.current_turn_index + 1) % self.track_length
            self.update_target_position()
            self.update_minimap(self.current_turn_index)
        self.game.after(50, self.move_object)

    def check_hit(self, event):
        pos = self.canvas.coords(self.rect)
        car_center = self.car_width // 2 
        if self.target_position - car_center <= pos[0] <= self.target_position + car_center:
            score = max(100 - abs(self.target_position - pos[0]), 0)
            self.total_score += score
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.total_score}")

    def update_target_position(self):
        self.target_position = random.randint(100, self.canvas_width - 100)
        if hasattr(self, 'target_line'):
            self.canvas.coords(self.target_line, self.target_position, 50, self.target_position, 150)
        else:
            self.target_line = self.canvas.create_line(self.target_position, 50, self.target_position, 150, fill="red")

