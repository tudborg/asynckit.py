# -*- coding: utf-8 -*- 

import threading
from errors import AsyncValueError

class AsyncBase(object):
    pass

class AsyncValue(threading._Event, AsyncBase):
    """ AsyncValue is a threading.Event with an attached value"""

    def __init__(self):
        super(AsyncValue, self).__init__()
        self._value     = None
        self._exception = None

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


class AsyncAggregator(AsyncBase):
    """takes a list of AsyncValue and waits for all of them to be set before self is set"""
    def __init__(self, *iterable):
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

