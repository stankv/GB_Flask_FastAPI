# Создать программу, которая будет производить подсчет
# количества слов в каждом файле в указанной директории и
# выводить результаты в консоль.
# Используйте асинхронный подход.


from asyncio import ensure_future, gather, run
from os import listdir
from os.path import join, isfile
from time import time

directory = '.'
tasks = []
start_time = time()


async def file_listening(arg):
    f = join(directory, arg)
    words = 0
    if isfile(f):
        with open(f) as file:
            for line in file:
                words += len(line.split())
        print(
            f'\nFile: {f:>38}  \twords: {words:>5}'
            f' in {time() - start_time:.6f} seconds')


async def main(arg):
    for file_path in listdir(arg):
        task = ensure_future(file_listening(file_path))
        tasks.append(task)
    await gather(*tasks)


if __name__ == '__main__':
    run(main(directory))
