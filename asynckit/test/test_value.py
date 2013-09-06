import unittest

from ..value  import AsyncValue
from ..value  import AsyncAggregator
from ..errors import AsyncValueError
import time
import threading


class TestAsyncValue(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_async_value_basic(self):
        # out test value
        res = AsyncValue()
        self.assertEqual(res.get(), None)     # assert initial value is None
        self.assertFalse(res.is_set(), True)  # assert value is True
        res.set(True)                         # set value
        self.assertTrue(res.get(),    True)   # assert value is True
        self.assertTrue(res.is_set(), True)   # assert Event is set

    def test_get_wait(self):
        res = AsyncValue()
       
        def wait_and_set():  # our thread logic
            time.sleep(0.05)
            res.set(True)

        # start thread that waits 100ms and sets result
        start_time = time.time()
        threading.Thread(target=wait_and_set).start()
        # block until result is set
        res.wait()
        value = res.get()

        self.assertTrue(value)                                          # assert value is as we set it (True)
        self.assertAlmostEqual(time.time()-start_time, 0.05, delta=0.1) # assert time it tool is ~ time of wait


    def test_get_and_block(self):
        res = AsyncValue()

        def wait_and_set():  # our thread logic
            time.sleep(0.05)
            res.set(True)

        # start thread that waits 100ms and sets result
        start_time = time.time()
        threading.Thread(target=wait_and_set).start()
        # block until result is set
        value = res.get(True)
        self.assertTrue(value)                                          # assert value is as we set it (True)
        self.assertAlmostEqual(time.time()-start_time, 0.05, delta=0.1) # assert time it tool is ~ time of wait

    def test_set_twice(self):
        res = AsyncValue()
        res.set(True)                                      # call first time, should be ok
        self.assertRaises(AsyncValueError, res.set, True)  # call second time, should throw error
        self.assertRaises(AsyncValueError, res.set, True)  # call third time, should throw error

    def test_set_and_clear(self):
        res = AsyncValue()
        res.set(True)                                      # call first time, should be ok
        self.assertRaises(AsyncValueError, res.set, True)  # call second time, should throw error
        res.clear()                                        # clear value and event flag
        self.assertEqual(res.get(), None)                  # assert getting value now is None
        self.assertFalse(res.is_set())                     # assert flag is not set
        res.set(True)                                      # set again
        self.assertTrue(res.is_set())                      # assert flag is now set again
        self.assertTrue(res.get())                         # assert value is now True again
        
    def test_raises_if_value_is_exception(self):
        class TestCaseException(Exception): pass
        res = AsyncValue()
        res.set(None, TestCaseException('expected'))       # set value None, exception TestCaseException
        self.assertTrue(res.is_error())                    # assert that result is error (due to exception)
        self.assertRaises(TestCaseException, res.get)      # get exception should raise it
        self.assertRaises(TestCaseException, res.get)      # get again should still raise it

class TestAsyncAggregator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_aggregator_basic(self):
        # out test value
        v1 = AsyncValue()
        v2 = AsyncValue()
        v3 = AsyncValue()
        v4 = AsyncValue()

        #test create
        agg = AsyncAggregator(v1,v2)
        #test append
        agg.append(v3)
        agg.append(v4)

        #all false
        self.assertFalse(v1.is_set())
        self.assertFalse(v2.is_set())
        self.assertFalse(v3.is_set())
        self.assertFalse(v4.is_set())
        self.assertFalse(agg.is_set())

        v1.set()                       
        #v1 now set
        self.assertTrue(v1.is_set())
        self.assertFalse(v2.is_set())
        self.assertFalse(v3.is_set())
        self.assertFalse(v4.is_set())
        self.assertFalse(agg.is_set())

        v2.set()
        #v1 and v2 now set
        self.assertTrue(v1.is_set())
        self.assertTrue(v2.is_set())
        self.assertFalse(v3.is_set())
        self.assertFalse(v4.is_set())
        self.assertFalse(agg.is_set())

        agg.remove(v3)
        agg.remove(v4)
        v3.set()
        self.assertTrue(v1.is_set())
        self.assertTrue(v2.is_set())
        self.assertTrue(v3.is_set())
        self.assertFalse(v4.is_set())
        self.assertTrue(agg.is_set())

        #test clear all
        agg.clear()
        self.assertFalse(v1.is_set())
        self.assertFalse(v2.is_set())
        self.assertTrue(v3.is_set())
        self.assertFalse(v4.is_set())
        self.assertFalse(agg.is_set())

        #test set all
        agg.set()
        self.assertTrue(v1.is_set())
        self.assertTrue(v2.is_set())
        self.assertTrue(v3.is_set())
        self.assertFalse(v4.is_set())
        self.assertTrue(agg.is_set())

        #test isSet other name
        self.assertTrue(agg.isSet())

        #waiting should be free now
        agg.wait(timeout=1.0)
        self.assertTrue(agg.is_set())

