# Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
# Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
# Программа должна использовать многопоточный, многопроцессорный и
# асинхронный подходы.
# Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
# Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.

import os.path
from requests import get
from time import sleep, time
import argparse
from threading import Thread
from multiprocessing import Process
from asyncio import ensure_future, gather, run, create_task, get_event_loop
from aiohttp import ClientSession

# парсинг аргументов командной строки
def arg_parse():
    parser = argparse.ArgumentParser(description='Парсер изображений по URL-адресам')
    parser.add_argument('data', metavar='url1 url2 url3', type=str, nargs='*', help='Введите url-адреса, ' \
                        'разделяя их пробелами.')
    return parser.parse_args()


# создание папки для скачиваемых изображений
def create_folder(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)


# ф-я скачивания одного изображения (только для tread и proc)
def download_img(url, path):
        start_time = time()
        response = get(url)
        filename = os.path.basename(url)
        #sleep(0.1)
        with open(os.path.join(path, filename), "wb") as f:
            f.write(response.content)
            print(f"Загружен {filename} за {time() - start_time:.2f} сек.")


# декоратор для расчета общего времени загрузки изображений (только для tread и proc)
def all_time(func):
    def wrapper(*args):
        start_time = time()
        func(*args)
        print(f'Общее время загрузки: {time() - start_time:.2f} сек.')

    return wrapper


@all_time
def download_tread(urls):
    path = "Treading"
    create_folder(path)
    
    threads = []
    for url in urls:
        thread = Thread(target=download_img, args=[url, path], daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


@all_time
def download_proc(urls):
    path = "Proc"
    create_folder(path)
    
    processes = []
    for url in urls:
        process = Process(target=download_img, args=[url, path])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


async def download_async_img(url, path):
    start_time = time()
    async with ClientSession() as session:
        async with session.get(url) as response:
            filename = os.path.basename(url)
            item = await response.read()
            with open(os.path.join(path, filename), "wb") as f:
                f.write(item)
            print(f"Загружен {filename} за {time() - start_time:.2f} сек.")


async def download_async(urls):
    path = "Async"
    create_folder(path)

    tasks = []
    start_time = time()
    for url in urls:
        #task = ensure_future(download_async_img(url, path))
        task = create_task(download_async_img(url, path))
        tasks.append(task)
    await gather(*tasks)
    print(f'Общее время загрузки: {time() - start_time:.2f} сек.')



def main(urls):
    while True:
        print("Парсинг изображений.")
        if urls == []:
            print("Вы не задали url-адреса изображений.")
            print(f"Будет использован url-адрес {TEST_URL}")
            urls = [TEST_URL]
        print("Выберите метод скачивания:")
        print("1 - Thread\t2 - Multiprocessing\t3 - Async\tq - Выход")
        menu = input(">>> ")
        if menu.lower() == 'q':
            break
        elif menu == '1':
            download_tread(urls)
        elif menu == '2':
            download_proc(urls)
        elif menu == '3':
            #run(download_async(urls))    # при выходе из программы (ввод q) вызывает RuntimeError
            # Пишут что это связано с версией Python, на 3.10 это исправлено (у меня 3.8)
# Решение подсказано на https://stackoverflow.com/questions/65682221/runtimeerror-exception-ignored-in-function-proactorbasepipetransport
            get_event_loop().run_until_complete(download_async(urls))
        print()



if __name__ == '__main__':
    # url для запуска программы когда не заданы аргументы в командной строке
    TEST_URL = 'https://img.goodfon.ru/original/800x480/6/a6/kosmos-art-tumannosti-ogni.jpg'

    urls = arg_parse().data
    main(urls)

# Для тестов аргументы для запуска из командной строки:
# https://i.7fon.org/150/f61016203.jpg
# https://img.youtube.com/vi/96EuqgkXpJo/0.jpg
# https://bilimdiler.kz/oyin_sayk/uploads/posts/2023-03/1679903895_kosmos.jpg
# https://i.ytimg.com/vi/QSgV2dpqjmY/hqdefault.jpg
