# Создать программу, которая будет производить подсчет
# количества слов в каждом файле в указанной директории и
# выводить результаты в консоль.
# Используйте процессы


from multiprocessing import Process
from time import time
from os.path import join, isfile
from os import listdir

directory = '.'
processes = []
start_time = time()


def file_listening(arg):
    f = join(directory, arg)
    words = 0
    if isfile(f):
        with open(f, encoding='utf-8') as file:
            for line in file:
                words += len(line.split())
        print(f'\nFile: {f:>38}  \twords: {words:>5} in '
              f'{time() - start_time:.2f} seconds')


if __name__ == '__main__':
    for file_path in listdir(directory):
        process = Process(target=file_listening, args=[file_path])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()