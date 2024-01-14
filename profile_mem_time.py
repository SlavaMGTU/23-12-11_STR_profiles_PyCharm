
import time
from itertools import combinations
import tracemalloc

# Запускаем отслеживание памяти
tracemalloc.start()

# Фиксируем начальное время
start_time = time.time()

# Здесь можно разместить код, время выполнения которого необходимо измерить
def get_comb(arr):
    for v in arr:
        for c in combinations((a for a in arr if a != v), 2):
            yield v, *c

for _ in range(1000):
    for no, c in enumerate(get_comb([10, 11, 12, 13])):
        print(c[0], c[1], c[2])

# Фиксируем конечное время
end_time = time.time()

# Измеряем количество использованной памяти
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

# Выводим топ-10 ресурсоемких строк кода
for stat in top_stats[:10]:
    print(stat)

# Вычисляем время выполнения, вычитая начальное время из конечного
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд")
