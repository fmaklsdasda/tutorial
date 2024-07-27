import os
import json
from tkinter import Tk, Frame

from pages.game_menu import GameMenu
from pages.game_settings import (
    BAN_NAMES,
    MIN_NAME_LENGTH,
    STANDARD_PLAYER_NAME,
    GameSettings,
)


class Game(Tk):
    def __init__(self):
        super().__init__()
        self.settings_file = "settings.json"
        self.player_name = ""
        self.player_color = ""
        self.load_settings()

        self.container = Frame(self)

        # TODO: investigate this lines, what a hell does it means!
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # TODO: setup main layout - page size Width x Height

        self.pages = {}

        self.open_menu()

    def open_page(self, Page):
        name = Page.__name__
        page = None
        if name in self.pages:
            page = self.pages[name]
        else:
            page = Page(game=self)
            self.pages[name] = page

        self.active_page = page
        self.active_page.grid(row=0, column=0, sticky="nsew")
        self.active_page.tkraise()

    def start_game(self):
        print("игра начата")

    def open_menu(self):
        self.open_page(GameMenu)

    def open_settings(self):
        self.open_page(GameSettings)

    # TODO: add new about page with version

    # Handle game exit
    def quit_app(self):
        print("вы вышли из приложения")

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


game = Game()
game.mainloop()
