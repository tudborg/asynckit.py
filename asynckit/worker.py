
import threading
import Queue
from errors import InvalidWorkTypeError


class Worker(threading.Thread):

    def __init__(self, scheduled_work):
        super(Worker, self).__init__()
        self.daemon          = True
        self.scheduled_work  = scheduled_work
        self.stop_event      = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            work = None
            try:
                event, work, args, kwargs = self.scheduled_work.get(True, 0.1)
            except Queue.Empty:
                continue
            
            if callable(work):
                try:
                    result = work(*args, **kwargs)
                except Exception, e:
                    result = e
            else:
                result = InvalidWorkTypeError("work should be instance of callable or WorkerCommand, was of type {}".format(type(work)))

            #set event with result
            event.set(result)
