from random import uniform
from socket import AF_INET, SHUT_RDWR, SOCK_STREAM, socket
from time import sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger
    from threading import Event


def work(index: int, event: "Event", logger: "Logger") -> None:
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
