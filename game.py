import os
import json
from tkinter import Tk, Frame

from config import GAME_HEIGHT, GAME_WIDTH
from pages.game_page import MovingGame
from pages.game_menu import GameMenu
from pages.game_settings import (
    BAN_NAMES,
    MIN_NAME_LENGTH,
    STANDARD_PLAYER_NAME,
    GameSettings,
)


class Game(Tk):
    def __init__(self, width, height):
        super().__init__()
        self.settings_file = "settings.json"
        self.player_name = ""
        self.player_color = ""
        self.load_settings()
        self.active_page = None
        
        self.geometry(f"{width}x{height}")
        self.container = Frame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        self.open_menu()

    def open_page(self, Page):
        name = Page.__name__
        page = None
        # if name in self.pages:
        #     page = self.pages[name]
            
        # else:
        #     page = Page(game=self)
        #     self.pages[name] = page
        page = Page(game=self)
        
        if self.active_page:
            if hasattr(self.active_page, "unmount"):
               self.active_page.unmount()
        

        self.active_page = page
        self.active_page.grid(row=0, column=0, sticky="nsew")
        self.active_page.tkraise()

    def open_game(self):
        self.open_page(MovingGame)

    def open_menu(self):
        self.open_page(GameMenu)

    def open_settings(self):
        self.open_page(GameSettings)

    def quit_app(self):
        exit()

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


game = Game(GAME_WIDTH, GAME_HEIGHT)
game.mainloop()
