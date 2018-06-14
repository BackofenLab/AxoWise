import urllib.request

def get(url):
    return urllib.request.urlopen(url).read().decode("utf-8")
