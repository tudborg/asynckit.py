[![Build Status](https://travis-ci.org/tbug/asynckit.py.png?branch=master)](travis)
[![Coverage Status](https://coveralls.io/repos/tbug/asynckit.py/badge.png?branch=master)](coveralls)
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

The return value of the `.do()` method is an object of type `AsyncValue`.
The `AsyncValue` is a `threading.Event` with the added bonus of being able to
carry a value.

When your work completes, the return value will be stored in the `AsyncValue` object
ready for retrieval.

Before you retrieve your value, ensure that the work is completed by checking if the
`AsyncValue` object is set with the `.is_set()` method.

You can also wait for the result by calling the objects `.wait()` method.

See [http://docs.python.org/2/library/threading.html#event-objects]() for how to work
with the `AsyncValue` object as a `threading.Event`.

When you are ready to retrieve your value, call the `AsyncValue` object's `.get()` method.

Alternatively you can call `.get()` with a timeout in seconds to block and wait for the result.
This is identical to calling `.wait()` just before calling `.get()`.

`.get()` returns the return value of your work, or raise an exception thrown inside your work.


### Joining multiple AsyncValues

Usually you want to perform n times work in parallel, and wait for all of it to complete.

This can be achieved with the `AsyncList` object:

```python
from asynckit import Pool, AsyncList
import urllib2

# define our heavy work
def download(url):
    return urllib2.urlopen(url).read()    

# create a pool
pool = Pool(worker_count=2)

# then schedule the heavy work on the pool
result1 = pool.do(download, 'http://tudb.org')
result2 = pool.do(download, 'http://github.com')
result3 = pool.do(download, 'http://tudb.org')

# then we create an AsyncList with our AsyncValues in it
my_downloads = AsyncList([result1, result2, result3])

# The AsyncList is itself an AsyncValue, with is_set() and wait()
# We could call .wait() on our list to wait for the results to complete
# my_downloads.wait()

# or we can simply tell the .get() method to wait by passing True as first argument
# the .get() method returns a list of values stored in our AsyncValue results
print [len(site) for site in my_downloads.get(True)]
```

### Chaining Work

In 0.4 the `.chain()` methods was introduced, allowing you to chain work in a more natural way.

`.chain()` works just like a `Pool`s `.do()` method, except it will wait until complete before scheduling
your chained work:

```python
from asynckit import Pool
import urllib2

def download(url):
    return urllib2.urlopen(url).read()

pool = Pool()

# the final result will only contain the return value of the _last_ chain call
final_result = pool.do(download, 'http://tudb.org').chain(download, 'http://tudb.org')

print len(final_result.get(True))
```


[coveralls]:    https://coveralls.io/r/tbug/asynckit.py?branch=master
[travis]:       https://travis-ci.org/tbug/asynckit.py