import os
import json


MIN_NAME_LENGTH = 3
STANDARD_PLAYER_NAME = "Petya"

class Game:
    def __init__(self):
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

    def run(self):
        while True:
            self.clear_console()
            self.show_menu()

    def exit(self):
        print("\nКорректный выход из игры...")
        exit()

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        print("1. Начать игру")
        print("2. Настройки")
        print("3. Выход")
        choice = input("Выберите пункт меню: ")

        if choice == "1":
            self.start_game()
        elif choice == "2":
            self.settings()
        elif choice == "3":
            self.exit()
        else:
            print("Некорректный выбор, попробуйте еще раз.")

    def start_game(self):
        print("Игра началась! (Но пока ничего не происходит)")

    def settings(self):
        def insert_name(counter = 0):
            if counter >= 3:
                print("что то у тебя не выходит, тебя будут звать {}".format(STANDARD_PLAYER_NAME))
                return STANDARD_PLAYER_NAME
            player_name = input(f"Введите имя игрока (не меньше {MIN_NAME_LENGTH} символов): ")
            if len(player_name) <= MIN_NAME_LENGTH:
                print("Неверное имя пользователя. Попробуйте еще раз.")
                return insert_name(counter + 1)
            return player_name
        while True:
            self.clear_console()
            print("Настройки:")

            player_name = insert_name()
            player_color = input(f"Введите цвет игрока {", ".join(list(self.colors.keys()))}: ").lower()
            if player_color in self.colors:
                rgb_color = self.colors[player_color]
                print(f"Имя: {self.player_name}, Цвет: {self.player_color}, RGB: {rgb_color}")
            else:
                print("Некорректный цвет. Попробуйте еще раз.")
                continue

            choice = input("Сохранить настройки? (y/n, Esc для отмены): ").lower()
            if choice == 'y':
                self.player_color = player_color
                self.player_name = player_name
                self.save_settings()
                print("Настройки сохранены.")
                break
            elif choice == 'esc':
                break
            else:
                print("Настройки не сохранены. Попробуйте снова.")
                continue

    def save_settings(self):
        settings = {
            "player_name": self.player_name,
            "player_color": self.player_color,
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.player_name = settings.get("player_name", "")
                self.player_color = settings.get("player_color", "")

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        game.exit()
