from tkinter import Canvas, ttk, Tk, Label, Frame, ALL


class GameMenu(Frame):
    def __init__(self, game) -> None:
        Frame.__init__(self, game.container)
        self.game = game
        self.mount()
        self.grid(row=0, column=0, sticky="nsew")

    def mount(self):
        game = self.game
        label = Label(self, text ="asdaf")
        label.pack()
        button_start = ttk.Button(self, text="Начать игру", command=game.start_game)
        button_settings = ttk.Button(self, text="Настройки", command=game.open_settings)
        button_exit = ttk.Button(self, text="Выход", command=game.quit_app)
        button_start.pack(pady=10)
        button_settings.pack(pady=10)
        button_exit.pack(pady=10)

    def unmount(self):
        pass
