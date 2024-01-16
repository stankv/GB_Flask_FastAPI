# Создать программу, которая будет производить подсчет
# количества слов в каждом файле в указанной директории и
# выводить результаты в консоль.
# Используйте потоки.


from os import listdir
from os.path import join, isfile
from threading import Thread
from time import time

directory = '.'    # текущая директория
threads = []
start_time = time()


def print_time(func):
    def wrapper(*args):
        start_time = time()
        func(*args)
        print(f'in {time() - start_time:.2f} sec')

    return wrapper


# подсчет числа слов в файле
def file_listening(arg):    # arg - путь до файла
    f = join(directory, arg)    #  полный путь до файла
    words = 0
    if isfile(f):
        with open(f, encoding='utf-8') as file:
            for line in file:
                words += len(line.split())
        print(f'\nFile: {f:>38}  \twords: {words:>5} ')


@print_time
def loop_func():
    for file_path in listdir(directory):
        thread = Thread(target=file_listening, args=[file_path])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


loop_func()
