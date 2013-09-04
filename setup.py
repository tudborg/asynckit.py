
from setuptools import setup, find_packages
import asynckit
import time

def stamp():
    return time.strftime('%j%H%M')

long_description = """
AsyncKit is a micro-toolkit for doing async work in python.
(in your otherwise hacked togethe synchronous single-file script)
"""

setup(
    name             = 'asynckit',
    version          = asynckit.__version__+'-r{}'.format(stamp()), #autostamp to avoid overwriting old versions accidentally
    description      =  'AsyncKit is a micro-toolkit for doing async work in python',
    author           = asynckit.__author__,
    author_email     = asynckit.__email__,
    license          = asynckit.__license__,
    url              = 'https://github.com/tbug/asynckit.py',
    keywords         = 'async utility util asynckit helper',
    packages         = find_packages(exclude=['test*']),
    install_requires = [
        'nose==1.3',
        'coverage==3.6',
        'python-coveralls==2.4.0'
    ],
    long_description = long_description
)
