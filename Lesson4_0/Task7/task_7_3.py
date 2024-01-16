from asyncio import ensure_future, gather, run
from random import randint
from time import time

start_time = time()
processes = []

arr = [randint(0, 101) for i in range(1, 1000001)]


async def arr_sum(arg):
    res = sum(arg)
    print(f"{res} calculated in {time() - start_time:.2f} seconds")


async def main():
    tasks = []
    for i in range(5):
        task = ensure_future(arr_sum(arr))
        tasks.append(task)
    await gather(*tasks)


if __name__ == '__main__':
    run(main())
