from urllib.request import Request, urlopen
from xml.etree import ElementTree as etree
from datetime import date, datetime, timedelta


pub_format = '%a, %d %b %Y %H:%M:%S'
today = date.today()
week_start = today - timedelta(days=8)
week_end = today - timedelta(days=1)


def is_recent(item):
    pub_date = item.findtext('pubDate')
    date_str = pub_date[:pub_date.rfind(' ')]
    date = datetime.strptime(date_str, pub_format).date()
    return week_start <= date and date <= week_end


def parse_item(item):
    title = item.findtext('title')
    link = item.findtext('link')
    return {"title": title, "link": link}


def parse_blog(src):
    blog_xml = etree.fromstring(src)
    title = blog_xml.findall('channel')[0].findtext('title')
    items = blog_xml.findall('channel/item')
    recent = filter(is_recent, items)
    items = [parse_item(item) for item in recent]
    return {"title": title, "items": items}


def download_feed(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request) as response:
        html = response.read().decode('utf-8')
    return html


def lambda_handler(event, context):
    blogs = event.get('blogs', [])

    url = event['urls'].pop()
    xml = download_feed(url)
    blogs.append(parse_blog(xml))

    return {
        'email_from': event['email_from'],
        'email_to': event['email_to'],
        'urls': event['urls'] or -1,
        'blogs': blogs
    }