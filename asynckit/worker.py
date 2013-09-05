
import threading
import Queue
from errors import InvalidWorkTypeError, RescheduleException
from value  import AsyncValue


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
            exception = None
            result = None

            try:
                event, work, args, kwargs = self.scheduled_work.get(True, 0.1)
            except Queue.Empty:
                continue

            if callable(work):
                try:
                    # check if any of the args are instance of AsyncValue
                    # and resolve if possible, else reschedule work
                    new_args = []
                    for arg in args:
                        if isinstance(arg, AsyncValue):
                            if arg.is_set(): new_args.append(arg.get())
                            else:            raise RescheduleException()
                        else: new_args.append(arg)

                    new_kwargs = {}
                    for key,value in kwargs.items():
                        if isinstance(value, AsyncValue):
                            if value.is_set(): new_kwargs[key] = value.get()
                            else:              raise RescheduleException()
                        else: new_kwargs[key] = value

                    result = work(*new_args, **new_kwargs)
                #if reschedule exception, reschedule and continue
                except RescheduleException as e:
                    self.scheduled_work.put( (event, work, args, kwargs) )
                    continue
                except Exception as e:
                    exception = e
            else:
                exception = InvalidWorkTypeError("work should be instance of callable or WorkerCommand, was of type {}".format(type(work)))

            #set event with result
            event.set(result, exception)
