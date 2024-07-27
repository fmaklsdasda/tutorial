from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, messagebox, Frame

STANDARD_PLAYER_NAME = "Игрок"
MIN_NAME_LENGTH = 3
BAN_NAMES = {"admin", "player", "Hitler"}
COLORS = {
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF"
}

class GameSettings:
    def __init__(self, game) -> None:
        self.game = game
        self.player_name = StringVar()
        self.player_color = StringVar()
        self.player_color.set(next(iter(COLORS.keys())))
        self.mount()

    def validate_name(self, name):
        if not name:
            return False, "Имя не может быть пустым."
        if name[0].isdigit():
            return False, "Первый символ не может быть числом."
        if len(name) < MIN_NAME_LENGTH:
            return False, f"Имя должно содержать не меньше {MIN_NAME_LENGTH} символов."
        if name.lower() in BAN_NAMES:
            return False, "Это имя запрещено."
        return True, ""

    def mount(self):
        game = self.game
        window = game.window
        window.title("Настройки")

        Label(window, text="Введите имя игрока:").pack()
        Entry(window, textvariable=self.player_name).pack()

        Label(window, text="Выберите цвет игрока:").pack()
        OptionMenu(window, self.player_color, *COLORS.keys()).pack()

        Button(window, text="Сохранить настройки", command=self.save_settings).pack()

    def save_settings(self):
        player_name = self.player_name.get()
        valid, message = self.validate_name(player_name)

        if not valid:
            messagebox.showerror("Ошибка", message)
            return

        player_color = self.player_color.get()
        if player_color not in COLORS:
            messagebox.showerror("Ошибка", "Некорректный цвет.")
            return

        self.game.player_name = player_name
        self.game.player_color = player_color
        self.game.save_settings()

        messagebox.showinfo("Успех", "Настройки сохранены.")
        self.game.window.destroy()

class Game(Tk):
    def __init__(self) -> None:
        self.frame = Frame(self)
        self.player_name = STANDARD_PLAYER_NAME
        self.player_color = ""

    def save_settings(self):
        print(f"Имя: {self.player_name}, Цвет: {self.player_color}, RGB: {COLORS[self.player_color]}")

    def start_settings(self):
        GameSettings(self)
        self.frame.mainloop()

if __name__ == "__main__":
    game = Game()
    game.start_settings()