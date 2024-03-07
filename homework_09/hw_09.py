import os
import threading
import time
from multiprocessing import Process
from pathlib import Path
from threading import Thread

import requests

image_url = "https://picsum.photos/1000/1000"
path = Path("rockyou.txt")


def encrypt_file(path: Path):
    start = time.perf_counter()
    print(f"Processing file from {path} in process {os.getpid()}")
    _ = [i for i in range(100_000_000)]
    encryption_time = time.perf_counter() - start
    print(f"Processing file took {encryption_time} seconds")
    return encryption_time


def download_image(image_url: str):
    start = time.perf_counter()
    print(
        f"Downloading image from {image_url} in thread"
        f"{threading.current_thread().name}"
    )
    response = requests.get(image_url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)
    download_time = time.perf_counter() - start
    print(f"Downloading image took {download_time} seconds")
    return download_time


if __name__ == "__main__":
    print("Sequential execution")
    try:
        start_encryption_seq = time.perf_counter()
        encrypt_file(path)
        encryption_time_seq = time.perf_counter() - start_encryption_seq

        total_download_time_seq = 0

        for i in range(5):
            download_time_seq = download_image(image_url)
            total_download_time_seq += download_time_seq

        total_seq = encryption_time_seq + total_download_time_seq

        print(
            f"Time taken for CPU-bound encryption task: "
            f"{encryption_time_seq} seconds\n"
            f"I/O-bound task: {total_download_time_seq} seconds\n"
            f"Total: {total_seq} seconds"
        )
    except Exception as e:
        print(f"Error occurred: {e}")

    print("\nParallel execution")
    try:
        start_encryption_par = time.perf_counter()

        process = Process(target=encrypt_file, args=(path,))
        process.start()
        process.join()

        encryption_time_par = time.perf_counter() - start_encryption_par

        start_download_par = time.perf_counter()

        threads = [
            Thread(target=download_image, args=(image_url,)) for _ in range(5)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        download_time_par = time.perf_counter() - start_download_par

        total_par = encryption_time_par + download_time_par

        print(
            f"Time taken for CPU-bound encryption task: "
            f"{encryption_time_par} seconds\n"
            f"I/O-bound task: {download_time_par} seconds\n"
            f"Total: {total_par} seconds"
        )
    except Exception as e:
        print(f"Error occurred: {e}")
