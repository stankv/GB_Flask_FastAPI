from multiprocessing import Process
from random import randint
from time import time

start_time = time()
processes = []

arr = [randint(0, 101) for i in range(1, 1000001)]


def arr_sum(arg):
    res = sum(arg)
    print(f"{res} calculated in {time() - start_time:.2f} seconds")


if __name__ == '__main__':
    for i in range(5):
        p = Process(target=arr_sum, args=(arr,), daemon=True)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()