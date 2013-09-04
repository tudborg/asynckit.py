[![Build Status](https://travis-ci.org/tbug/asynckit.py.png?branch=master)](https://travis-ci.org/tbug/asynckit.py)
[![Coverage Status](https://coveralls.io/repos/tbug/asynckit.py/badge.png?branch=master)](https://coveralls.io/r/tbug/asynckit.py?branch=master)
asynckit.py
===========

AsyncKit is a micro-toolkit for doing async work in python 
(in your otherwise hacked togethe synchronous single-file script)

Usage
----------

### The Pool

Import the Pool:
```python
from asynckit import Pool
```

Create a pool object with your desired number of workers
```python
my_pool = Pool(worker_count=4)
```

### Add some work

You hand a pool a callable.
The easiest way is by defining a function.
You will be able to retrieve the return value later,
and any exception raised inside your work be be caught
and stored until you are ready for the result of your work to be retrieved,
where it will be re-raised.

Let's add some work
```python
def download_url(url):
    return urllib2.urlopen(url).read()

asyncResultObject = my_pool.do(download_url, 'http://www.python.org/')
```
Here we tell `my_pool` to call `download_url` with the argument `'http://www.python.org/'`.
You can add as many arguments as you like, and even keyword arguments like you would expect from any regular function call.

The return value of the `.do()` method is an object of type `AsyncResult`.
The `AsyncResult` is a `threading.Event` with the added bonus of being able to
carry a value.

When your work completes, the return value will be stored in the `AsyncResult` object
ready for retrieval.

Before you retrieve your value, ensure that the work is completed by checking if the
`AsyncResult` object is set with the `.is_set()` method.

You can also wait for the result by calling the objects `.wait()` method.

See [http://docs.python.org/2/library/threading.html#event-objects]() for how to work
with the `AsyncResult` object as a `threading.Event`.

When you are ready to retrieve your value, call the `AsyncResult` object's `.get()` method.

Alternatively you can call `.get()` with a timeout in seconds to block and wait for the result.
This is identical to calling `.wait()` just before calling `.get()`.

`.get()` returns the return value of your work, or raise an exception thrown inside your work.

### Chaining Work

You can chain work simply by using an `AsyncResult` object as the value for other work.
The work will automatically be handled when all resuls are ready, or when an exception is
thrown in one of the results.

```python

a = AsyncResult()
b = AsyncResult()

# schedule some work with the arguments: a,1,b,2
# (2 out of 4 arguments are AsyncResult objects)
myAsyncResult = pool.do(work, a, 1, b, 2)

# set the value of out AsyncResult objects
a.set("my A value")  # pool still missing b value
b.set("my B value")  # pool will do work here
```



Example
----------
```python
from asynckit import Pool
import urllib2

my_pool = Pool(worker_count=3)

# work to run in pool
def download_url(url):
    return urllib2.urlopen(url).read()

# add work to pool
pypiDownload   = my_pool.do(download_url, 'https://pypi.python.org/pypi/asynckit/0.1.0')
githubDownload = my_pool.do(download_url, 'https://github.com/tbug/asynckit.py')
pythonDownload = my_pool.do(download_url, 'http://www.python.org/')

# wait for downloads
pypiDownload.wait()
githubDownload.wait()
pythonDownload.wait()

# get value from out completed work
# NOTE: get() will re-throw any exception not handled inside your work
pypiPage = pypiDownload.get()
githubPage = githubDownload.get()
pythonPage = pythonDownload.get()

print "downloaded {} bytes from pypi.python.org".format(len(pypiPage))
print "downloaded {} bytes from github.com".format(len(githubPage))
print "downloaded {} bytes from python.org".format(len(pythonPage))

# stop pool, block until pool is stopped
my_pool.stop(True)

```