import logging
from concurrent.futures import ThreadPoolExecutor
from random import uniform
from socket import AF_INET, SHUT_RDWR, SOCK_STREAM, socket
from threading import Event
from time import sleep

logger = logging.getLogger("pool_client")


def work(index: int, event: "Event") -> None:
    sleeping_time = round(uniform(1, 2), 2)  # noqa: S311
    client = socket(AF_INET, SOCK_STREAM)
    # with socket(AF_INET, SOCK_STREAM) as client:
    logger.critical("%d connecting...", index)
    client.connect(("127.0.0.1", 8000))
    logger.critical("%d connected!", index)
    while not event.is_set():
        logger.critical("%d waiting for data...", index)
        client.recv(1024)  # blocking
        logger.critical("%d received data, now sleeping for %.2f", index, sleeping_time)
        client.sendall(b"hello")
        sleep(sleeping_time)
    logger.critical("%d CLOSING", index)
    client.shutdown(SHUT_RDWR)
    client.close()
    logger.critical("%d CLOSED", index)



with ThreadPoolExecutor(max_workers=2, thread_name_prefix="main_pool") as executor:
    stop = Event()
    executor.submit(work, 0, stop)
    executor.submit(work, 1, stop)
    executor.submit(work, 2, stop)
    sleep(3)

    logger.critical(">>> setting stop")
    stop.set()
    sleep(3)


logger.critical("end")
