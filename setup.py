
from setuptools import setup, find_packages
import asynckit

setup(
    name         = 'asynckit',
    version      = asynckit.__version__,
    description  =  '''AsyncKit is a micro-toolkit for doing async work in python 
                   (in your otherwise hacked togethe synchronous single-file script)''',
    author       = asynckit.__author__,
    author_email = asynckit.__email__,
    license      = asynckit.__license__,
    url          = 'https://github.com/tbug/asynckit.py',
    keywords     = 'async utility util asynckit helper',
    packages     = find_packages(exclude=['test*'])
)
