import os
import json
import shutil
import time

MIN_NAME_LENGTH = 3
STANDARD_PLAYER_NAME = "Petya"
BAN_NAMES = ["admin", "root", "Hitler"]
MIN_TERMINAL_WIDTH = 80
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
        os.system("cls" if os.name == "nt" else "clear")

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
        self.animate_marker(0.4)

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

    def get_terminal_width(self):
        return shutil.get_terminal_size().columns
    
    def terminal_width_check(self):
        terminal_size = shutil.get_terminal_size((80,20))
        current_terminal_width = terminal_size.columns
        if current_terminal_width < MIN_TERMINAL_WIDTH:
            print("Ширина терминала не подходит")
        else:
            print("Ширина терминала подходит")

    def animate_marker(self, speed):
        marker = "-"
        while True:
            terminal_width = self.get_terminal_width()
            length = terminal_width // 2
            for position in range(length):
                self.clear_console()
                print(" " * position + marker)
                time.sleep(speed)
            for position in range(length - 2, 0, -1):
                self.clear_console()
                print(" " * position + marker)
                time.sleep(speed)


if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        game.exit()
