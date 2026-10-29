"""Прогноз методом Monte Carlo: скільки спринтів потрібно, щоб закрити залишок points.

Одна симуляція: беремо залишок і, поки він більший за нуль, випадково тягнемо
одне число зі списку velocity, віднімаємо його і рахуємо спринт. Коли залишок
дійшов до нуля або нижче, записуємо кількість спринтів. Повторюємо багато разів.
"""
import math
import random

SIMULATIONS = 10000
SEED = 2026          # фіксуємо, щоб прогін можна було повторити і отримати ті самі числа
MAX_SPRINTS = 200    # запобіжник на випадок, якщо у списку самі нулі


def simulate(remaining, velocities, simulations=SIMULATIONS, seed=SEED):
    rng = random.Random(seed)
    results = []
    for _ in range(simulations):
        left = remaining
        sprints = 0
        while left > 0 and sprints < MAX_SPRINTS:
            left -= rng.choice(velocities)   # випадковий спринт з нашої історії
            sprints += 1
        results.append(sprints)
    results.sort()
    return percentile(results, 0.50), percentile(results, 0.85)


def percentile(sorted_results, p):
    # число, нижче або на рівні якого лежить частка p результатів
    index = math.ceil(p * len(sorted_results)) - 1
    return sorted_results[index]


if __name__ == "__main__":
    # Навчальні дані курсу (lr09_reference_velocity.csv, points_done по 12 спринтах).
    # Це вигадана навчальна команда, моїх даних тут немає.
    reference = [21, 17, 26, 14, 23, 6, 28, 12, 22, 25, 18, 9]
    print("Навчальні дані курсу, обсяг 220 points")
    for name, data in (("усі 12 спринтів", reference),
                       ("спринти 1 і 2", reference[0:2]),
                       ("спринти 5 і 6", reference[4:6])):
        p50, p85 = simulate(220, data)
        print(f"  {name}: velocity {data}, P50 = {p50}, P85 = {p85}")

    # Мої дані: velocity двох спринтів з velocity.csv
    mine = [16, 16]
    print("Мої дані, velocity", mine)
    for name, remaining in (("весь перший реліз", 59), ("залишок після двох спринтів", 27)):
        p50, p85 = simulate(remaining, mine)
        print(f"  {name}: {remaining} points, P50 = {p50}, P85 = {p85}")
