asynckit.py
===========

AsyncKit is a micro-toolkit for doing async work in python 
(in your otherwise hacked togethe synchronous single-file script)

Usage
----------



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