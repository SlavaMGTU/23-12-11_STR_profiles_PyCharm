import tracemalloc

# Запускаем отслеживание памяти
tracemalloc.start()

# Код, вызывающий потенциально затратный по памяти процесс
from itertools import combinations


def get_comb(arr):
    for v in arr:
        for c in combinations((a for a in arr if a != v), 2):
            yield v, *c


for no, c in enumerate(get_comb([10, 11, 12, 13])):
    print(c[0], c[1], c[2])

# Измеряем количество использованной памяти
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

# Выводим топ-10 ресурсоемких строк кода
for stat in top_stats[:10]:
    print(stat)


