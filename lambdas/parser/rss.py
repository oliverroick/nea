from datetime import datetime
from .util import is_recent

pub_format = '%a, %d %b %Y %H:%M:%S'


def parse_item(item):
    title = item.findtext('title')
    link = item.findtext('link')

    pub_date = item.findtext('pubDate')
    date_str = pub_date[:pub_date.rfind(' ')]
    date = datetime.strptime(date_str, pub_format).date()

    return {"title": title, "link": link, "date": date}


def parse(blog_xml):
    title = blog_xml.findall('channel')[0].findtext('title')
    items = blog_xml.findall('channel/item')
    parsed_items = (parse_item(item) for item in items)
    recent = filter(is_recent, parsed_items)
    return {"title": title, "items": recent}
