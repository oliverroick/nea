from urllib.request import Request, urlopen


def download_feed(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request) as response:
        html = response.read()
    return html


def get_feeds(urls):
    return [download_feed(url) for url in urls]
