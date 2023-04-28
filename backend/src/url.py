"""
Module containing HTTP(S) request helpers.
"""

import time
import urllib.error
from urllib.request import urlopen, Request

from utils import throttle

_MIN_WAIT = 1 # second(s)

@throttle(_MIN_WAIT)
def get(url, timeout=10):
    try:
        return urlopen(url, timeout = timeout).read().decode(encoding = "utf-8", errors = "ignore")
    except Exception as e:
        print(e)
        return None

@throttle(_MIN_WAIT)
def post(url, data, timeout=20):
    request = Request(url, data, method="POST")
    try:
        return urlopen(request, timeout = timeout).read().decode(encoding = "utf-8", errors = "ignore")
    except Exception as e:
        print(e)
        return None
