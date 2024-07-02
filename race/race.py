import random


class Kart:
    def __init__(self, color):
        self.color = color
        # random.uniform - это средняя скорость которая была выбрана исходя из личного опыта
        self.avg_speed = random.uniform(20, 40)  
        print(
            f"{self.color} kart is ready with an average speed of {self.avg_speed:.2f} km/h"
        )  # .2f определяет количество знаков после запятой (2 знака)

    def go(self):
        print(f"{self.color} kart is started")

    def race_time(self, loops, loop_length):
        total_distance = loops * loop_length
        time = total_distance / self.avg_speed * 60
        return time


class Race:
    def __init__(self, karts, loops, loop_length):
        self.karts = karts
        self.laps = loops
        self.lap_length = loop_length
        for kart in karts:
            print(f"{kart.color} kart added to the race")  

    def start(self):
        for kart in self.karts:
            kart.go()

    def get_result(self):
        results = []
        for kart in self.karts:
            time = kart.race_time(self.laps, self.lap_length)
            results.append((kart.color, time))

        results.sort(key=lambda x: x[1])  # строчная функция сортировки по времени
        return results[:3]  # возрврат данных о первых трех местах


# я немного изменил из за того, что первый вариант не работал в этом случае
red_kart = Kart("red")
blue_kart = Kart("blue")
green_kart = Kart("green")
orange_kart = Kart("orange")

race = Race(
    [red_kart, blue_kart, green_kart, orange_kart], loops= 17, loop_length= 1.3
) 
race.start()

results = race.get_result()
print("Top 3 results:")
for position, (color, time) in enumerate(results, 1):
    print(f"{position}. {color} kart with time {time:.2f} minutes")
