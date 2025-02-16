import time
from urllib.parse import urlparse
from urllib.request import urlopen


def get(url, timeout=10, wait=1):
    if type(wait) is int and wait > 0:
        time.sleep(wait)

    parsed_url = urlparse(url)
    if parsed_url.scheme not in ["http", "https"]:
        raise ValueError("URL scheme must be http or https")

    try:
        return urlopen(url, timeout=timeout).read().decode(encoding="utf-8", errors="ignore")  # nosec
    except:
        return None
