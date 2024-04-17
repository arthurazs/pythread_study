import logging
from threading import Event, Thread
from time import sleep

from base import work

logger = logging.getLogger("threading_client")

stop = Event()

for index in range(3):
    thread = Thread(target=work, args=(index, stop, logger))
    thread.start()

sleep(3)

logger.critical(">>> setting stop")
stop.set()
sleep(3)

logger.critical("end")
