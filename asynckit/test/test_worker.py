import unittest

from ..value  import AsyncValue
from ..worker import Worker
from ..errors import WorkerError, InvalidWorkTypeError
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


    def test_worker_does_work_with_async_value(self):
        q = Queue.Queue()                         # queue
        worker = Worker(q)                        # create worker
        worker.start()                            # start worker
        res = AsyncValue()
        def work(a,b):
            return a+b

        a = AsyncValue()
        b = AsyncValue()
        a.set(1)
        b.set(2)

        #put a work tuple in queue
        q.put( (res, work, [a,b], {}) )
        res.wait(timeout=0.2)                     # wait for work to complete (max 200ms)
        self.assertTrue(res.is_set())             # assert that value is set after wait returns
        self.assertEqual(res.get(), 3)            # assert that work actually added 1 and 2

    def test_worker_handles_reschedule(self):
        q = Queue.Queue()                         # queue
        worker = Worker(q)                        # create worker
        worker.start()                            # start worker
        res = AsyncValue()
        def work(a,b,c):
            return a+b+c

        a = AsyncValue()
        b = AsyncValue()
        
        a.set(1)
        #b.set(2)                                 # don't set be to trigger reschedule

        #put a work tuple in queue
        q.put( (res, work, [a,b,1], {}) )
        res.wait(timeout=0.1)                     # wait for work to (not) complete
        self.assertFalse(res.is_set())            # work not complete yes due to missing value

        b.set(2)                                  # set the missing value
        res.wait(timeout=0.2)                     # wait for result, this time it should complete

        self.assertTrue(res.is_set())             # assert result was actually set
        self.assertEqual(res.get(), 4)            # assert result is the correct value ( 1+2+1 = 3 )

    def test_worker_handles_reschedule_kwargs_version(self):
        q = Queue.Queue()                         # queue
        worker = Worker(q)                        # create worker
        worker.start()                            # start worker
        res = AsyncValue()
        def work(a,b,c):
            return a+b+c

        a = AsyncValue()
        b = AsyncValue()
        
        a.set(1)
        #b.set(2)                                 # don't set be to trigger reschedule

        #put a work tuple in queue
        q.put( (res, work, [], {'a': a, 'b': b, 'c': 1}) )
        res.wait(timeout=0.1)                     # wait for work to (not) complete
        self.assertFalse(res.is_set())            # work not complete yes due to missing value

        b.set(2)                                  # set the missing value
        res.wait(timeout=0.2)                     # wait for result, this time it should complete

        self.assertTrue(res.is_set())             # assert result was actually set
        self.assertEqual(res.get(), 4)            # assert result is the correct value ( 1+2+1 = 4 )
