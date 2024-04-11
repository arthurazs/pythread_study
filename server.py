from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform
from threading import Event
from socket import socket, AF_INET, SOCK_STREAM
import logging

logger = logging.getLogger("pool_server")


def work() -> None:
    with socket(AF_INET, SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 8000))
        server.listen(1)
        logger.critical("Listening on port 8000")
        while True:
            connection, address = server.accept()
            with connection:
                logger.critical("Accepted %s", address)
                while True:
                    # connection.sendall(b"hi")
                    connection.recv(1024)


work()
