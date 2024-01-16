# Написать программу, которая считывает список из 10 URL-
# адресов и одновременно загружает данные с каждогоадреса.
# После загрузки данных нужно записать их в отдельные файлы.
# Используйте процессы.


from requests import get
from time import time
from multiprocessing import Process

urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        'https://ru.wikipedia.org/',
        'https://ru.hexlet.io/',
        'https://megaseller.shop/',
        'https://linux.org',
        'https://metanit.com/',
        ]


def download(url):
    response = get(url)
    filename = 'proc_' + url.replace('https://', '').replace('.', '_').replace(
        '/', '') + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time() - start_time:.2f}seconds")


processes = []
start_time = time()
if __name__ == '__main__':    # при работе с процессами этот блок необходим
    for url in urls:
        process = Process(target=download, args=(url,), daemon=True)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
