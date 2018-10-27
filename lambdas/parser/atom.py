from datetime import datetime
from .util import is_recent

pub_format = '%Y-%m-%dT%H:%M:%S'

ns = {
    'atom': 'http://www.w3.org/2005/Atom'
}


def get_timezone_index(timestamp):
    if timestamp.rfind('Z') != -1:
        return timestamp.rfind('Z')
    elif timestamp.rfind('+') != -1:
        return timestamp.rfind('+')
    elif timestamp.rfind('-') != -1:
        return timestamp.rfind('-')
    else:
        return len(timestamp)


def parse_item(item):
    title = item.find('atom:title', ns).text
    link = item.find('atom:link', ns).attrib['href']

    pub_date = item.find('atom:published', ns).text
    timezone_index = get_timezone_index(pub_date)
    date_str = pub_date[:timezone_index]
    date = datetime.strptime(date_str, pub_format).date()

    return {"title": title, "link": link, "date": date}


def parse(blog_xml):
    title = blog_xml.findtext('{http://www.w3.org/2005/Atom}title')
    items = blog_xml.findall('atom:entry', ns)
    parsed_items = (parse_item(item) for item in items)
    recent = filter(is_recent, parsed_items)

    return {"title": title, "items": list(recent)}
