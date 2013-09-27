import unittest

from ..value  import AsyncValue, AsyncList
from ..errors import AsyncValueError
import time
import threading


class TestAsyncList(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_empty(self):
        # out test value
        al = AsyncList()
        self.assertFalse(al.is_error()) #no error
        self.assertTrue(al.is_set())    #list is set if all (no) values is set
        self.assertRaises(AsyncValueError, al.set)
        self.assertRaises(AsyncValueError, al.clear)

    def test_has_items(self):
        l = [
            AsyncValue(),
            AsyncValue()
        ]
        al = AsyncList(l)
        self.assertEqual(len(al._value), 2) #just to be sure, 2 items expected

        self.assertFalse(al.is_error()) #no error
        self.assertFalse(al.is_set())   #list has items, so not set

        l[0].set() #set first item

        self.assertFalse(al.is_error()) #no error
        self.assertFalse(al.is_set())   #list still has one item not set

        l[1].set()

        self.assertFalse(al.is_error()) #no error
        self.assertTrue(al.is_set())

        l[0].clear() #clearing one should unset the list

        self.assertFalse(al.is_error()) #no error
        self.assertFalse(al.is_set())


    def test_append(self):
        l = [
            AsyncValue(),
            AsyncValue()
        ]
        al = AsyncList(l)
        self.assertEqual(len(al._value), 2) #just to be sure, 2 items expected
        l[0].set()
        l[1].set()
        self.assertFalse(al.is_error())
        self.assertTrue(al.is_set())
        newValue = AsyncValue()
        l.append(newValue)
        self.assertFalse(al.is_error())
        self.assertFalse(al.is_set())
        newValue.set()
        self.assertFalse(al.is_error())
        self.assertTrue(al.is_set())


    def test_get_wait(self):
        l = [
            AsyncValue(),
            AsyncValue()
        ]
        al = AsyncList(l)
       
        def wait_and_set():  # our thread logic
            time.sleep(0.05)
            l[0].set(1)
            l[1].set(2)

        # start thread that waits 100ms and sets result
        start_time = time.time()
        threading.Thread(target=wait_and_set).start()
        # block until result is set
        al.wait()
        values = al.get()
        self.assertEqual(values, [1,2])
        self.assertAlmostEqual(time.time()-start_time, 0.05, delta=0.1) # assert time it tool is ~ time of wait


    def test_get_and_block(self):
        l = [
            AsyncValue(),
            AsyncValue()
        ]
        al = AsyncList(l)

        def wait_and_set():  # our thread logic
            time.sleep(0.05)
            l[0].set(1)
            l[1].set(2)

        # start thread that waits 100ms and sets result
        start_time = time.time()
        threading.Thread(target=wait_and_set).start()
        # block until result is set
        values = al.get(True)
        self.assertEqual(values, [1,2])
        self.assertAlmostEqual(time.time()-start_time, 0.05, delta=0.1) # assert time it tool is ~ time of wait