__author__     = "Henrik Tudborg"
__license__    = "MIT"
__version__    = "0.1.0"
__maintainer__ = "Henrik Tudborg"
__email__      = "henrik@tudb.org"

# Pesky custom exceptions stored here for easy access
class AsyncKitError(Exception):          pass
#Value
class AsyncValueError(AsyncKitError):    pass
#Worker
class WorkerError(AsyncKitError):        pass
class InvalidWorkTypeError(WorkerError): pass
