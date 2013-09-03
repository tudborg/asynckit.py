
# Pesky custom exceptions stored here for easy access
class AsyncKitError(Exception):           pass
#Value
class AsyncValueError(AsyncKitError):     pass
#Worker
class WorkerError(AsyncKitError):         pass
class InvalidWorkTypeError(WorkerError):  pass
#
class RescheduleException(AsyncKitError): pass
