from xml.etree import ElementTree as etree
from . import rss, atom, util


class UnsupportedFeedType(Exception):
    pass


def parse_feed(xml):
    # Workaround for malformed content in Rand's blog
    xml = xml.replace('', '')

    parsed_xml = etree.fromstring(xml)

    if parsed_xml.tag == 'rss':
        feed_parser = rss
    elif parsed_xml.tag in ('feed', '{http://www.w3.org/2005/Atom}feed'):
        feed_parser = atom
    else:
        raise UnsupportedFeedType(parsed_xml.tag)

    parsed_blog = feed_parser.parse(parsed_xml)
    parsed_blog['items'] = list(map(util.serialisable, parsed_blog['items']))[:10]

    return parsed_blog
