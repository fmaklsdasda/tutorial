import random
import matplotlib.pyplot as plt


class Kart:
    def __init__(self, color):
        self.color = color
        self.lap_times = []  # список для хранения времени за каждый круг

    def go(self):
        print(f"{self.color} kart is started")

    def lap_time(self, lap_length):
        # генерируем случайное время для прохождения круга, время круга основано на личном опыте
        time = lap_length / random.uniform(46, 56) * 60
        self.lap_times.append(time)
        return time

    def avg_speed(self, lap_length):
        # рассчитываем среднюю скорость
        total_time = sum(self.lap_times)
        total_distance = len(self.lap_times) * lap_length
        avg_speed = total_distance / (total_time / 60)
        return avg_speed


class Race:
    def __init__(self, karts, laps, lap_length):
        self.karts = karts
        self.laps = laps
        self.lap_length = lap_length
        for kart in karts:
            print(f"{kart.color} kart added to the race")

    def start(self):
        for kart in self.karts:
            kart.go()
            for _ in range(self.laps):
                kart.lap_time(self.lap_length)

    def get_result(self):
        results = []
        for kart in self.karts:
            total_time = sum(kart.lap_times)
            results.append((kart.color, total_time, kart.avg_speed(self.lap_length)))

        results.sort(key=lambda x: x[1])  # сортировка по времени
        return results[:3]  # возврат данных о первых трех местах


# создание объектов картов
red_kart = Kart("red")
blue_kart = Kart("blue")
green_kart = Kart("green")
orange_kart = Kart("orange")

# создание объекта гонки
race = Race([red_kart, blue_kart, green_kart, orange_kart], laps=17, lap_length=1.3)
race.start()

# получение результатов
results = race.get_result()
print("Top 3 results:")
for position, (color, total_time, avg_speed) in enumerate(results, 1):
    print(
        f"{position}. {color} kart with total time {total_time:.2f} minutes and average speed {avg_speed:.2f} km/h"
    )
