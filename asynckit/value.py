# -*- coding: utf-8 -*- 

import threading
from errors import AsyncValueError

class AsyncValue(threading._Event):
    """ AsyncValue is a threading.Event with an attached value"""

    def __init__(self):
        super(AsyncValue, self).__init__()
        self._value = None

    def clear(self):
        """ clear event and value """
        super(AsyncValue, self).clear()
        self._value = None

    def set(self, value):
        """set value (this also sets the event, just like a set() call to a regular event)
           value can be any value. If instance of Exception, it will be re-raised when
           someone tries to get the value"""
        if self.is_set():
            raise AsyncValueError('value already set')
        self._value = value
        super(AsyncValue, self).set()

    def get(self, timeout=None):
        """get the value, block until value is ready or until timeout if timeout is set
           if timeout is 0, block forever"""
        #figure out if we should block, and what the timeout should be
        should_block   = timeout is not None and (timeout == True or isinstance(timeout, (int,float)))
        actual_timeout = timeout if isinstance(timeout, (int,float)) else None

        if should_block and not self.is_set():
            self.wait(actual_timeout)
        if isinstance(self._value, Exception):
            raise self._value
        else:
            return self._value
