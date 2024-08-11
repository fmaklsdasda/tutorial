import tkinter as tk
import time
import random
import math

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
        self.canvas_height = height // 2
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.rect = self.canvas.create_rectangle(20, 80, 40, 100, fill="blue")

        self.update_target_position()

        self.moving_speed = 10
        self.direction = 1
        self.start_time = time.time()
        self.game.bind("<s>", self.check_hit)
        self.game.bind("<space>", self.highlight_turn)
        self.total_score = 0
        self.score_text = self.canvas.create_text(self.canvas_width // 2, self.canvas_height - 20, text=f"Score: {self.total_score}", font=("Arial", 16))

        self.move_object()

        tk.Button(self, text="В меню", command=self.game.open_menu).pack()

        # Mini-map setup
        self.minimap_width = 200
        self.minimap_height = 200
        self.minimap = tk.Canvas(self, width=self.minimap_width, height=self.minimap_height, bg="white")
        self.minimap.pack()
        self.turn_points = self.generate_track_points()
        self.current_turn = 0
        self.draw_track()

    def unmount(self):
        self.game.unbind("<s>")
        self.game.unbind("<space>")

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

    def generate_track_points(self):
        num_turns = 7
        center_x, center_y = self.minimap_width // 2, self.minimap_height // 2
        radius = 80
        points = []
        angle = 0

        for _ in range(num_turns):
            while True:
                angle += random.randint(30, 120)
                x = center_x + radius * math.cos(math.radians(angle))
                y = center_y + radius * math.sin(math.radians(angle))
                new_point = (x, y)

                # Check for intersection with existing lines
                if not self.check_intersection(points, new_point):
                    points.append(new_point)
                    break

        # Close the loop
        points.append(points[0])
        return points

    def check_intersection(self, points, new_point):
        if len(points) < 2:
            return False

        for i in range(len(points) - 1):
            if self.lines_intersect(points[i], points[i + 1], points[-1], new_point):
                return True
        return False

    def lines_intersect(self, p1, p2, p3, p4):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    def draw_track(self):
        self.turn_markers = []
        for i in range(len(self.turn_points) - 1):
            self.minimap.create_line(self.turn_points[i][0], self.turn_points[i][1], self.turn_points[i + 1][0], self.turn_points[i + 1][1], fill="black")
            marker = self.minimap.create_oval(self.turn_points[i][0] - 3, self.turn_points[i][1] - 3, self.turn_points[i][0] + 3, self.turn_points[i][1] + 3, fill="red")
            self.turn_markers.append(marker)
        
        marker = self.minimap.create_oval(self.turn_points[-1][0] - 3, self.turn_points[-1][1] - 3, self.turn_points[-1][0] + 3, self.turn_points[-1][1] + 3, fill="red")
        self.turn_markers.append(marker)

    def highlight_turn(self, event):
        self.minimap.itemconfig(self.turn_markers[self.current_turn], fill="red")

        self.current_turn = (self.current_turn + 1) % len(self.turn_points)
        
        self.minimap.itemconfig(self.turn_markers[self.current_turn], fill="green")
