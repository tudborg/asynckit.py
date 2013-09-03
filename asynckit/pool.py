# -*- coding: utf-8 -*- 

import threading
import Queue
from worker import Worker
from value  import AsyncValue


class Pool(object):
    """"A Pool of worker threads to do async work """
    def __init__(self, worker_count=1):
        super(Pool, self).__init__()
        self.scheduled_work   = Queue.Queue()
        self.stop_event       = threading.Event()
        self._workers         = []

        [self._schedule_worker_start() for i in range(worker_count)]

    @property
    def worker_count(self):
        """get number of current workers"""
        return len(self._workers)

    @worker_count.setter
    def worker_count(self, value):
        """set the intended worker count. Pool will automatically start or stop required workers"""
        if isinstance(value, int):
            diff = value - self.worker_count
            if diff > 0:  # new number larger, add workers
                for i in range(abs(diff)):
                    self._schedule_worker_start()
            elif diff < 0:  # new number lower, remove workers
                for i in range(abs(diff)):
                    self._schedule_worker_stop()
        else:
            raise TypeError('expected int, got {}'.format(type(value)))

    def _schedule_worker_start(self):
        """start one new worker"""
        worker = Worker(self.scheduled_work)
        worker.start()
        self._workers.append( worker )
        return worker

    def _schedule_worker_stop(self):
        """stop one old worker"""
        worker = self._workers.pop()
        worker.stop()
        return worker

    def do(self, work, *args, **kwargs):
        """ do work with *args and **kwargs where work is instance of callable
            do() returns an AsyncValue object.
            the AsyncValue object is a threading.Event that sets a value when the event is set.
            see threading.Event documentation for possible methods.
            AsyncValue has the additional get() method that retrieves the value (or None if not set) """
        result = AsyncValue()
        self.scheduled_work.put( (result, work, args, kwargs) )
        return result

    def stop(self, timeout=None):
        """ stop workers, return list of worker threads. Will block if timeout is number
            will block without timeout if timeout is 0"""

        # accept bools indication if should block
        if timeout is True:
            timeout = 0
        elif timeout is False:
            timeout = None

        if isinstance(timeout, (int,float)):
            # blocking code
            [worker.stop() for worker in self._workers]
            [worker.join(timeout if timeout > 0 else None) for worker in self._workers]
            workers = self._workers
            self._workers = []
            return workers
        else:
            # non-blocking code (default)
            return [self._schedule_worker_stop() for i in range(len(self._workers))]
