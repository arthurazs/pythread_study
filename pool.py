import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from time import sleep

from base import work

logger = logging.getLogger("pool_client")


with ThreadPoolExecutor(max_workers=2, thread_name_prefix="main_pool") as executor:
    stop = Event()
    executor.submit(work, 0, stop, logger)
    executor.submit(work, 1, stop, logger)
    executor.submit(work, 2, stop, logger)
    sleep(3)

    logger.critical(">>> setting stop")
    stop.set()
    sleep(3)


logger.critical("end")
