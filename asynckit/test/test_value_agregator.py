import unittest

from ..value  import AsyncValue
from ..value  import AsyncAggregator
from ..errors import AsyncValueError
import time
import threading


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


    def test_aggregator_is_error(self):
        class TestCaseException(Exception):pass
        v1 = AsyncValue()
        v2 = AsyncValue()
        agg = AsyncAggregator(v1,v2)
        v1.set(True)
        v2.set(exception=TestCaseException())
        #v2 has error and is in aggregator so agg is error
        self.assertTrue(agg.is_error())
        #remove problem
        agg.remove(v2)
        #should now pass
        self.assertFalse(agg.is_error())
