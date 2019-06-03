"""
Module containing HTTP(S) request helpers.
"""

import time
import urllib.error
from urllib.request import urlopen


def get(url, timeout = 10, wait = 1):
    if isinstance(wait, int) and wait > 0:
        time.sleep(wait)
    try:
        return urlopen(url, timeout = timeout).read().decode(encoding = "utf-8", errors = "ignore")
    except Exception as e:
        print(e)
        return None
