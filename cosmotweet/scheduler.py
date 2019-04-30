from datetime import datetime
from datetime import timedelta
from threading import Thread




def _do_after_wait(func, args, wait_time):
    start_time = datetime.now()
    while datetime.now() <= start_time + timedelta(seconds=wait_time):
        pass

    try:
        func(*args)
    except TypeError:
        func(args)


def _schedule(func, args, wait_time):
    thread = Thread(target=_do_after_wait, args=(func, args, wait_time))
    thread.start()
