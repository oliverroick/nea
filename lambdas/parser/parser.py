from xml.etree import ElementTree as etree
from . import rss, atom


class UnsupportedFeedType(Exception):
    pass


def parse_feed(xml):
    parsed_xml = etree.fromstring(xml)

    if parsed_xml.tag == 'rss':
        feed_parser = rss
    elif parsed_xml.tag == 'feed':
        feed_parser = atom
    else:
        raise UnsupportedFeedType(parsed_xml.tag)

    return feed_parser.parse(parsed_xml)
