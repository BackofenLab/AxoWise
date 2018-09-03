from urllib.request import urlopen
import urllib.error
import time

def get(url, timeout = 10, wait = 1):
    if type(wait) is int and wait > 0:
        time.sleep(wait)
    try:
        return urlopen(url, timeout = timeout).read().decode(encoding = "utf-8", errors = "ignore")
    except:
        return None
