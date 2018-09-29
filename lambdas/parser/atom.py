from datetime import datetime
from .util import is_recent

pub_format = '%Y-%m-%dT%H:%M:%S'


def parse_item(item):
    title = item.findtext('title')
    link = item.find('link').attrib['href']

    pub_date = item.findtext('published')
    timezone_index = (pub_date.rfind('+') if pub_date.rfind('+') != -1
                      else pub_date.rfind('-'))
    date_str = pub_date[:timezone_index]
    date = datetime.strptime(date_str, pub_format).date()

    return {"title": title, "link": link, "date": date}


def parse(blog_xml):
    title = blog_xml.findtext('title')
    items = blog_xml.findall('entry')
    parsed_items = (parse_item(item) for item in items)
    recent = filter(is_recent, parsed_items)
    return {"title": title, "items": recent}
