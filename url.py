"""
Module containing HTTP(S) request helpers.
"""

import time
import urllib.error
from urllib.request import urlopen

from utils import throttle

_MIN_WAIT = 1 # second(s)

@throttle(_MIN_WAIT)
def get(url, timeout = 10):
    try:
        return urlopen(url, timeout = timeout).read().decode(encoding = "utf-8", errors = "ignore")
    except Exception as e:
        print(e)
        return None
