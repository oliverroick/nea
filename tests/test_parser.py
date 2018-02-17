from xml.etree import ElementTree as etree
from datetime import datetime, timedelta
from nea.parser import parse_blog, parse_item, is_recent, pub_format


yesterday = datetime.now() - timedelta(days=1)
last_week = yesterday - timedelta(days=8)

src = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:webfeeds="http://webfeeds.org/rss/1.0" version="2.0">
  <channel>
    <title>Test Blog</title>
    <item>
      <title>Post title 1</title>
      <link>http://example.com/1</link>
      <pubDate>{} +0000</pubDate>
    </item>
    <item>
      <title>Post title 2</title>
      <link>http://example.com/2</link>
      <pubDate>{} +0000</pubDate>
    </item>
  </channel>
</rss>
""".format(yesterday.strftime(pub_format), last_week.strftime(pub_format))


def test_is_recent():
    src_xml = etree.fromstring(src)
    items = src_xml.findall('channel/item')

    assert is_recent(items[0]) is True
    assert is_recent(items[1]) is False


def test_parse_blog():
    parsed = parse_blog(src)
    assert parsed.title == 'Test Blog'
    assert len(parsed.items) == 1


def test_parse_item():
    src_xml = etree.fromstring(src)
    items = src_xml.findall('channel/item')

    parsed = parse_item(items[0])
    assert parsed.title == 'Post title 1'
    assert parsed.link == 'http://example.com/1'
