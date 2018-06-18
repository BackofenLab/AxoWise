import urllib.request
import urllib.parse

def get(url):
    return urllib.request.urlopen(url).read().decode("utf-8")

def url_escape(string, safe = "/"):
    return urllib.parse.quote_plus(string, safe = safe)

def url_encode(obj, safe = "/"):
    return urllib.parse.urlencode(obj, safe = safe)
