import logging
from asyncio import get_event_loop, run
from socket import AF_INET, SOCK_STREAM, socket

logger = logging.getLogger("pool_server")


async def handle(connection: "socket") -> None:
    loop = get_event_loop()
    while True:
        try:
            await loop.sock_recv(connection, 1024)
        except ConnectionResetError:
            break
        try:
            await loop.sock_sendall(connection, b"hi")
        except BrokenPipeError:
            break


async def serve() -> None:
    with socket(AF_INET, SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 8000))
        server.listen(1)
        server.setblocking(False)  # noqa: FBT003
        loop = get_event_loop()
        logger.critical("Listening on port 8000")
        tasks = []
        while True:
            connection, address = await loop.sock_accept(server)
            logger.critical("Accepted %s", address)
            task = loop.create_task(handle(connection))
            tasks.append(task)
            task.add_done_callback(tasks.remove)

run(serve())
