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
    logger.critical("%d connecting...", index)
    client.connect(("127.0.0.1", 8000))
    logger.critical("%d connected!", index)
    broken = False
    while not event.is_set():
        logger.critical("%d sending data...", index)
        try:
            client.sendall(b"hello")
        except BrokenPipeError:
            broken = True
            logger.critical("%d ERROR WHILE SENDING", index)
            break
        logger.critical("%d receiving data...", index)
        data = client.recv(1024)  # blocking
        if data:
            logger.critical("%d received data %s, now sleeping for %.2f", index, data, sleeping_time)
        else:
            broken = True
            logger.critical("%d ERROR WHILE RECVING", index)
            break
        sleep(sleeping_time)
    if not broken:
        logger.critical("%d CLOSING", index)
        client.shutdown(SHUT_RDWR)
    client.close()
    logger.critical("%d CLOSED", index)
