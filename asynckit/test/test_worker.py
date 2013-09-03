import unittest

from ..value  import AsyncValue
from ..worker import Worker
from ..       import WorkerError, InvalidWorkTypeError
import time
import threading
import Queue


class TestWorkerCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_worker_thread_basics(self):
        q = Queue.Queue()                         # queue
        worker = Worker(q)                        # create worker
        worker.start()                            # start worker
        self.assertTrue(worker.is_alive())        # assert worker is alive
        worker.stop()                             # set stop event
        worker.join(timeout=0.2)                  # join worker, should never take more than 200ms
        self.assertFalse(worker.is_alive())       # assert worker not alive

    def test_worker_does_work(self):
        q = Queue.Queue()                         # queue
        worker = Worker(q)                        # create worker
        worker.start()                            # start worker
        res = AsyncValue()
        def work(a,b):
            return a+b
        #put a work tuple in queue
        q.put( (res, work, [1,2], {}) )
        res.wait(timeout=0.2)                     # wait for work to complete (max 200ms)
        self.assertTrue(res.is_set())             # assert that value is set after wait returns
        self.assertEqual(res.get(), 3)            # assert that work actually added 1 and 2

    def test_worker_handles_exception(self):
        class TestCaseError(Exception): pass
        q = Queue.Queue()                         # queue
        worker = Worker(q)                        # create worker
        worker.start()                            # start worker
        res = AsyncValue()
        def work(a,b):
            raise TestCaseError('expected')
        #put a work tuple in queue
        q.put( (res, work, [1,2], {}) )
        res.wait(timeout=0.2)                     # wait for work to complete (max 200ms)
        self.assertTrue(res.is_set())             # assert that value is set after wait returns
        self.assertRaises(TestCaseError, res.get) # assert that exception is re-raised

    def test_worker_handles_bad_work(self):
        class TestCaseError(Exception): pass
        q = Queue.Queue()                         # queue
        worker = Worker(q)                        # create worker
        worker.start()                            # start worker
        res = AsyncValue()
        work = "This is a string, not a callable"
        #put a work tuple in queue
        q.put( (res, work, [1,2], {}) )
        res.wait(timeout=0.2)                     # wait for work to complete (max 200ms)
        self.assertTrue(res.is_set())             # assert that value is set after wait returns
        self.assertRaises(InvalidWorkTypeError, res.get) # assert that exception is re-raised
