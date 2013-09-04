import unittest

from ..value  import AsyncValue
from ..worker import Worker
from ..pool   import Pool
from ..errors import WorkerError, InvalidWorkTypeError
import time
import threading
import Queue


class TestPoolCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pool_start_stop_blocking(self):
        # test that pool starts and stops workers as expected
        p = Pool()
        workers = p.stop(timeout=0.2)
        for worker in workers:
            self.assertFalse(worker.is_alive())

    def test_pool_start_stop_blocking_bool_arg(self):
        # test that pool starts and stops workers as expected
        p = Pool()
        workers = p.stop(True)       # True is shortcut for block-forever
        for worker in workers:
            self.assertFalse(worker.is_alive())

    def test_pool_start_stop_nonblocking(self):
        # test that pool starts and stops workers as expected
        p = Pool()
        workers = p.stop(None)       # non blocking
        for worker in workers:
            worker.join(timeout=0.2) # give each worker 200ms to stop
            self.assertFalse(worker.is_alive())

    def test_pool_start_stop_nonblocking_bool_arg(self):
        # test that pool starts and stops workers as expected
        p = Pool()
        workers = p.stop(False)      # false is shortcut for don't block at all
        for worker in workers:
            worker.join(timeout=0.2) # give each worker 200ms to stop
            self.assertFalse(worker.is_alive())

    def test_pool_scale(self):
        # test some basic scale-up and scale-down of worker pool
        p = Pool(worker_count=0)
        self.assertEqual(p.worker_count, 0)
        p.worker_count = 1
        self.assertEqual(p.worker_count, 1)
        p.worker_count = 2
        self.assertEqual(p.worker_count, 2)
        p.worker_count = 1
        self.assertEqual(p.worker_count, 1)

    def test_pool_scale_error(self):
        # test some basic scale-up and scale-down of worker pool
        p = Pool(worker_count=0)
        def test(): p.worker_count = "this is not a number"
        self.assertRaises(TypeError, test)

    def test_pool_work(self):
        # define some test work
        def mult(a,b): return a*b
        def add(a,b):  return a+b
        def div(a,b):  return a/b

        p = Pool(worker_count=0)  # get am empty pool
        p.worker_count = 3        # scale up

        expect9 = p.do(mult, 3,3) # add mult() work
        expect6 = p.do(add,  3,3) # add add() work
        expect1 = p.do(div,  3,3) # add div() work

        self.assertEqual(expect9.get(True), 9) 
        self.assertEqual(expect6.get(True), 6)
        self.assertEqual(expect1.get(True), 1)
