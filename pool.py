from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform
from threading import Event
from socket import socket, AF_INET, SOCK_STREAM
import logging

logger = logging.getLogger("pool_client")


def work(index: int, event: "Event") -> None:
    sleeping_time = round(uniform(1, 2), 2)
    with socket(AF_INET, SOCK_STREAM) as client:
        logger.critical("%d connecting...", index)
        client.connect(("127.0.0.1", 8000))
        logger.critical("%d connected!", index)
        while not event.is_set():
            logger.critical("%d waiting for data...", index)
            client.recv(1024)  # blocking
            logger.critical("%d received data, now sleeping for %.2f", index, sleeping_time)
            sleep(sleeping_time)
            client.sendall(b"hello")


with ThreadPoolExecutor(max_workers=2, thread_name_prefix="main_pool") as executor:
    stop = Event()
    executor.submit(work, 0, stop)
    executor.submit(work, 1, stop)
    executor.submit(work, 2, stop)
    sleep(5)

    logger.critical(">>> setting stop")
    stop.set()
    sleep(5)


logger.critical("end")
