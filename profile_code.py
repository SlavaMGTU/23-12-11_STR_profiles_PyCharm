from itertools import combinations
import time
# Импортируем декоратор для измерения использования памяти
from memory_profiler import profile

# Фиксируем начальное время
start_time = time.time()

def get_comb(arr):
    for v in arr:
        for c in combinations((a for a in arr if a != v), 2):
            yield v, *c

for no, c in enumerate(get_comb([10, 11, 12, 13])):

# Используем декоратор @profile для измерения использования памяти
@profile
def code_with_memory_profile():
    i = 0
    numbers = []
    while i < 1000000:
        numbers.append(i)
        i += 1
    return numbers


# Вызываем функцию для выполнения кода с профилированием памяти
result = code_with_memory_profile()






# Здесь можно разместить код, время выполнения которого необходимо измерить
# Например, простой цикл, который занимает некоторое время
for _ in range(1000000):
    pass  # Пропускаем выполнение кода

# Фиксируем конечное время
end_time = time.time()

# Вычисляем время выполнения, вычитая начальное время из конечного
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд")


