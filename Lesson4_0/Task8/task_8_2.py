from multiprocessing import Process
from time import time

from pywebcopy import save_website

processes = []
start_time = time()
urls = ['https://megaseller.shop/', ]


def website(url, folder='./'):
    name = 'proc_' + url.replace('https://', '').replace('.', '_').replace('/',
                                                                           '')
    save_website(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots=True,
        debug=True,
        delay=None,
    )
    print(f"Downloaded {url} in {time() - start_time:.2f} seconds")


if __name__ == '__main__':
    for url in urls:
        process = Process(target=website, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
