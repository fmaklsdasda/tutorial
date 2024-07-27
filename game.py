import os
import json
import shutil
import time
from tkinter import Canvas, ttk, Tk, Label, Frame, ALL
import random

from pages.game_menu import GameMenu
from pages.game_settings import GameSettings

MIN_NAME_LENGTH = 3
STANDARD_PLAYER_NAME = "Petya"
BAN_NAMES = ["admin", "root", "Hitler"]
GAME_WIDTH = 700
GAME_HEIGHT = 700


class Game(Tk):
    def __init__(self):
        super().__init__()
        self.settings_file = "settings.json"
        self.player_name = ""
        self.player_color = ""
        self.colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
        }
        self.load_settings()
        self.container = Frame(self)
        self.active_page = GameMenu(game=self)
        self.active_page.tkraise()

    def clear_window(self):
        if self.active_page:
            self.active_page.unmount()

    def start_game(self):
        print("игра начата")
    
    def open_settings(self):
        self.clear_window()
        self.active_page = GameSettings(game=self)
        
    def quit_app(self):
        print("вы вышли из приложения")

    def settings(self):
        def insert_name(counter=0):
            if counter >= 3:
                print(
                    "Что-то у тебя не выходит, тебя будут звать {}".format(
                        STANDARD_PLAYER_NAME
                    )
                )
                return STANDARD_PLAYER_NAME
            
             
            player_name = input(
                f"Введите имя игрока (не меньше {MIN_NAME_LENGTH} символов): "
            )
            
            if player_name and not player_name[0].isdigit():
                if len(player_name) >= MIN_NAME_LENGTH:
                    if player_name.lower() not in BAN_NAMES:
                        return player_name
                    else:
                        print("Это имя запрещено. Попробуйте еще раз.")
                else:
                    print("Неверное имя пользователя. Попробуйте еще раз.")
            else:
                print("Первый символ не может быть числом. Попробуйте еще раз.")
            
            return insert_name(counter + 1)

        while True:
            self.clear_console()
            print("Настройки:")

            player_name = insert_name()
            player_color = input(
                f"Введите цвет игрока {', '.join(list(self.colors.keys()))}: "
            ).lower()
            if player_color in self.colors:
                rgb_color = self.colors[player_color]
                print(
                    f"Имя: {self.player_name}, Цвет: {self.player_color}, RGB: {rgb_color}"
                )
            else:
                print("Некорректный цвет. Попробуйте еще раз.")
                continue

            choice = input("Сохранить настройки? (y/n, Esc для отмены): ").lower()
            if choice == "y":
                self.player_color = player_color
                self.player_name = player_name
                self.save_settings()
                print("Настройки сохранены.")
                break
            elif choice == "esc":
                break
            else:
                print("Настройки не сохранены. Попробуйте снова.")
                continue

    def save_settings(self):
        settings = {
            "player_name": self.player_name,
            "player_color": self.player_color,
        }
        with open(self.settings_file, "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                self.player_name = settings.get("player_name", "")
                self.player_color = settings.get("player_color", "")

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Настройки")
    settings_window.geometry("700x700")
    label = ttk.Label(settings_window, text="Здесь будут настройки")
    label.pack(pady=20)
    button_name = ttk.Button(settings_window, text="Имя игрока", command=settings_window.destroy)
    button_name.pack(pady=10)
    button_color = ttk.Button(settings_window, text="Выбор цвета игрока", command=settings_window.destroy)
    button_color.pack(pady=20)
    button_close = ttk.Button(settings_window, text="Закрыть", command=settings_window.destroy)
    button_close.pack(pady=30)

game = Game()
game.mainloop() 