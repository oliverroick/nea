from xml.etree import ElementTree as etree
from urllib.request import Request, urlopen
from .parser import rss


def download_feed(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request) as response:
        html = response.read().decode('utf-8')
    return html


def lambda_handler(event, context):
    blogs = event.get('blogs', [])

    url = event['urls'].pop()
    xml = download_feed(url)

    parsed_xml = etree.fromstring(xml)
    blogs.append(rss.parse(parsed_xml))

    return {
        'email_from': event['email_from'],
        'email_to': event['email_to'],
        'urls': event['urls'] or -1,
        'blogs': blogs
    }
