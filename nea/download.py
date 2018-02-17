import urllib2


def download_feed(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_feeds(urls):
    return [download_feed(url) for url in urls]
