# -*- coding: utf-8 -*- 

import threading
from errors import AsyncValueError

class AsyncValue(threading._Event):
    """ AsyncValue is a threading.Event with an attached value"""

    def __init__(self):
        super(AsyncValue, self).__init__()
        self._value     = None
        self._exception = None
        self._chains    = []    # [ (pool, result, callback, args, kwargs) ]
        self._pool      = None  # The pool this value is scheduled on if any

    def clear(self):
        """ clear event and value """
        super(AsyncValue, self).clear()
        self._value = None
        self._exception = None

    def set(self, value=None, exception=None):
        """set value (this also sets the event, just like a set() call to a regular event)
           value can be any value. If instance of Exception, it will be re-raised when
           someone tries to get the value"""
        if self.is_set():
            raise AsyncValueError('value already set')
        self._value = value
        self._exception = exception
        super(AsyncValue, self).set()

        self._trigger_chains()

    def get(self, timeout=None):
        """get the value, block until value is ready or until timeout if timeout is set
           if timeout is 0, block forever"""
        #figure out if we should block, and what the timeout should be
        should_block   = timeout is not None and (timeout == True or isinstance(timeout, (int,float)))
        actual_timeout = timeout if isinstance(timeout, (int,float)) else None

        if should_block and not self.is_set():
            self.wait(actual_timeout)
        if self._exception is not None:
            raise self._exception
        else:
            return self._value

    def is_error(self):
        return self._exception is not None


    # chain logic
    def pool_chain(self, pool, callback, *args, **kwargs):
        """return a new AsyncValue that will be set with the result value of callback"""
        result = AsyncValue()
        if self.is_set():
            pool._do(result, callback, *args, **kwargs)
        else:
            self._chains.append( (pool, result, callback, args, kwargs) )
        return result
    #chain shortcut for adding to pool used by self
    def chain(self, callback, *args, **kwargs):
        """chain a callback to be scheduled on self._pool when this value is ready"""
        return self.pool_chain(self._pool, callback, *args, **kwargs)

    def _trigger_chains(self):
        # handled chained logic
        while len(self._chains) > 0:
            pool, result, callback, args, kwargs = self._chains.pop(0) #pop in order of added
            (pool or self._pool)._do(result, callback, *args, **kwargs)


class AsyncList(AsyncValue):
    """ AsyncList contains 0 or more AsyncValues
        An AsyncList is set when all AsyncValues in the list is set.
        An AsyncList will raise an exception if one of it's elements raises an exception
        An AsyncList is itself an AsyncValue"""

    def __init__(self, l=[]):
        super(AsyncList, self).__init__()
        self._value = l

    def set(self, value=None, exception=None):
        raise AsyncValueError("AsyncList cannot be set directly")

    def clear(self, value=None, exception=None):
        raise AsyncValueError("AsyncList cannot be cleared")

    def get(self, timeout=None):
        """returns a list of values retrieved from AsyncValue elements
           time timeout is for each element, so maximum timeout is timeout*len(AsyncList)"""
        return [value.get(timeout) for value in self._value]

    def wait(self, timeout=None):
        """wait for all items to be set. timeout is per item"""
        for value in self._value:
            value.wait(timeout)

    def is_set(self):
        return next((False for v in self._value if not v.is_set()), True)

    isSet = is_set

    def is_error(self):
        """return True if one of it's children has error"""
        return next((True for v in self._value if v.is_error()), False)

    def pool_chain(self):
        raise AsyncValueError("you cannot yet chain on an AsyncList. Sorry")


class AsyncAggregator(AsyncList):
    """deprecated, Use AsyncList instead"""
    def __init__(self, *iterable):
        super(AsyncAggregator, self).__init__()
        self._values = [i for i in iterable]

    def append(self, value):
        return self._values.append(value)

    def remove(self, value):
        return self._values.remove(value)

    def set(self, *args, **kwargs):
        [value.set(*args, **kwargs) for value in self._values]

    def isSet(self):
        return self.is_set()

    def is_set(self):
        for value in self._values:
            if not value.is_set():
                return False
        return len(self._values) > 0  # will not appear set if no values is stored

    def clear(self, *args, **kwargs):
        [value.clear(*args, **kwargs) for value in self._values]

    def wait(self, *args, **kwargs):
        [value.wait(*args, **kwargs) for value in self._values]

    def is_error(self):
        for value in self._values:
            if hasattr(value, 'is_error') and value.is_error():
                return True
        return False
