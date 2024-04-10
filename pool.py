from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform
from threading import Event

def work(index: int, event: "Event") -> None:
    sleeping_time = round(uniform(0, 1), 2)
    while not event.is_set():
        print(index, "sleeping for", sleeping_time)
        sleep(sleeping_time)
        # input()  # how to kill threads with blocking io?

with ThreadPoolExecutor(max_workers=2, thread_name_prefix="main_pool") as executor:
    stop = Event()
    executor.submit(work, 0, stop)
    executor.submit(work, 2, stop)
    sleep(2)

    print(">>> setting stop")
    stop.set()
    sleep(2)

    print(">>> unsetting stop")
    stop.clear()

    executor.submit(work, 3, stop)
    sleep(2)

    print(">>> setting stop")
    stop.set()

print("end")
