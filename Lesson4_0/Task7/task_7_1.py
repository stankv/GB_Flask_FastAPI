# Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
#Использовать многопоточность.


from random import randint
from threading import Thread
from time import time

start_time = time()
threads = []

arr = [randint(0, 101) for i in range(1, 1000001)]


def arr_sum(arg):
    res = sum(arg)
    print(f"{res} calculated in {time() - start_time:.2f} seconds")


for i in range(5):
    t = Thread(target=arr_sum, args=[arr], daemon=True)
    threads.append(t)
    t.start()

if __name__ == '__main__':
    for t in threads:
        t.join()
