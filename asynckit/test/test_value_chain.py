import unittest

from ..value  import AsyncValue
from ..errors import AsyncValueError
from ..pool   import Pool
import time
import threading


class TestAsyncValue(unittest.TestCase):

    def setUp(self):
        self.pool = Pool(worker_count=1)

    def tearDown(self):
        self.pool.stop(2) #wait 2 seconds max for pool to stop

    def test_basic_chain(self):
        # out test value
        myList = []

        def addNumber(n):
            myList.append(n)

        done = self.pool.do(addNumber, 1).chain(addNumber, 2).chain(addNumber, 3)

        done.wait(0.3) # wait 300ms max for result
        self.assertTrue(done.is_set())
        self.assertFalse(done.is_error())
        self.assertEqual(sum(myList), 6)

    def test_chain_already_set(self):
        # out test value
        myList = []

        def addNumber(n):
            myList.append(n)

        semiDone = self.pool.do(addNumber, 1)
        semiDone.wait(0.1) # wait 100ms max for result
        #now chain the rest
        done = semiDone.chain(addNumber, 2).chain(addNumber, 3)
        done.wait(0.2)
        self.assertTrue(done.is_set())
        self.assertFalse(done.is_error())
        self.assertEqual(sum(myList), 6)
