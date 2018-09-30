import pytest
from xml.etree import ElementTree as etree
from datetime import date, timedelta
from unittest.mock import patch
from lambdas.parser import util, rss, atom, parser


# UTILS

def test_is_recent():
    pub_date = date.today() - timedelta(days=3)
    item = {'date': pub_date}
    assert util.is_recent(item) is True

    pub_date = date.today() - timedelta(days=17)
    item = {'date': pub_date}
    assert util.is_recent(item) is False


# RSS
def test_rss_parse_item():
    item_parameters = {
        'title': 'Some title',
        'link': 'http://example.com',
        'date': date(2018, 9, 17)
    }
    item_string = """
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <pubDate>Mon, 17 Sep 2018 00:00:00 +0000</pubDate>
            <description>Lots of words</description>
        </item>
    """
    item = etree.fromstring(item_string.format(**item_parameters))
    assert rss.parse_item(item) == item_parameters


def test_rss_parse():
    recent_date = date.today() - timedelta(days=3)
    recent_date_string = recent_date.strftime(rss.pub_format)

    older_date = date.today() - timedelta(days=17)
    older_date_string = older_date.strftime(rss.pub_format)

    item_string = """
        <rss>
            <channel>
                <title>Blog Title</title>
                <item>
                    <title>Title</title>
                    <link>http://example.com</link>
                    <pubDate>{recent_date} +0000</pubDate>
                    <description>Lots of words</description>
                </item>
                <item>
                    <title>Title</title>
                    <link>http://example.com</link>
                    <pubDate>{recent_date} +0000</pubDate>
                    <description>Lots of words</description>
                </item>
                <item>
                    <title>Title</title>
                    <link>http://example.com</link>
                    <pubDate>{older_date} +0000</pubDate>
                    <description>Lots of words</description>
                </item>
            </channel>
        </rss>
    """.format(recent_date=recent_date_string, older_date=older_date_string)

    parsed = rss.parse(etree.fromstring(item_string))
    assert parsed['title'] == 'Blog Title'
    assert len(list(parsed['items'])) == 2


# ATOM
def test_atom_parse_item():
    item_parameters = {
        'title': 'Some title',
        'link': 'http://example.com',
        'date': date(2018, 9, 17)
    }
    item_string = """
        <entry>
            <title>{title}</title>
            <link href="{link}" />
            <published>2018-09-17T00:00:00+00:00</published>
            <content>Lots of words</content>
        </entry>
    """
    item = etree.fromstring(item_string.format(**item_parameters))
    assert atom.parse_item(item) == item_parameters


def test_atom_parse_item_with_negative_time_diff():
    item_parameters = {
        'title': 'Some title',
        'link': 'http://example.com',
        'date': date(2018, 9, 17)
    }
    item_string = """
        <entry>
            <title>{title}</title>
            <link href="{link}" />
            <published>2018-09-17T00:00:00-02:00</published>
            <content>Lots of words</content>
        </entry>
    """
    item = etree.fromstring(item_string.format(**item_parameters))
    assert atom.parse_item(item) == item_parameters


def test_atom_parse():
    recent_date = date.today() - timedelta(days=3)
    recent_date_string = recent_date.strftime(atom.pub_format)

    older_date = date.today() - timedelta(days=17)
    older_date_string = older_date.strftime(atom.pub_format)

    item_string = """
        <feed>
            <title>Blog Title</title>
            <entry>
                <title>Title</title>
                <link href="http://example.com" />
                <published>{recent_date}+00:00</published>
                <content>Lots of words</content>
            </entry>
            <entry>
                <title>Title</title>
                <link href="http://example.com" />
                <published>{recent_date}+00:00</published>
                <content>Lots of words</content>
            </entry>
            <entry>
                <title>Title</title>
                <link href="http://example.com" />
                <published>{older_date}+00:00</published>
                <content>Lots of words</content>
            </entry>
        </feed>
    """.format(recent_date=recent_date_string, older_date=older_date_string)

    parsed = atom.parse(etree.fromstring(item_string))
    assert parsed['title'] == 'Blog Title'
    assert len(list(parsed['items'])) == 2


# PARSER
@patch('lambdas.parser.parser.rss')
@patch('lambdas.parser.parser.atom')
def test_parser_parse_rss(mocked_atom, mocked_rss):
    feed_string = """
        <rss>
            <channel>
                <title>Blog Title</title>
            </channel>
        </rss>
    """
    parsed_rss_blog = {'title': 'RSS Blog Title'}
    parsed_atom_blog = {'title': 'Atom Blog Title'}
    mocked_rss.parse.return_value = parsed_rss_blog
    mocked_atom.parse.return_value = parsed_atom_blog

    result = parser.parse_feed(feed_string)

    assert result == parsed_rss_blog
    mocked_rss.parse.assert_called_once()
    mocked_atom.parse.assert_not_called()


@patch('lambdas.parser.parser.rss')
@patch('lambdas.parser.parser.atom')
def test_parser_parse_atom(mocked_atom, mocked_rss):
    feed_string = """
        <feed>
            <title>Blog Title</title>
        </feed>
    """
    parsed_rss_blog = {'title': 'RSS Blog Title'}
    parsed_atom_blog = {'title': 'Atom Blog Title'}
    mocked_rss.parse.return_value = parsed_rss_blog
    mocked_atom.parse.return_value = parsed_atom_blog

    result = parser.parse_feed(feed_string)

    assert result == parsed_atom_blog
    mocked_rss.parse.assert_not_called()
    mocked_atom.parse.assert_called_once()


@patch('lambdas.parser.parser.rss')
@patch('lambdas.parser.parser.atom')
def test_parser_parse_unsupported(mocked_atom, mocked_rss):
    feed_string = """
        <unsupported>
            <title>Blog Title</title>
        </unsupported>
    """
    parsed_rss_blog = {'title': 'RSS Blog Title'}
    parsed_atom_blog = {'title': 'Atom Blog Title'}
    mocked_rss.parse.return_value = parsed_rss_blog
    mocked_atom.parse.return_value = parsed_atom_blog

    with pytest.raises(parser.UnsupportedFeedType):
        parser.parse_feed(feed_string)

    mocked_rss.parse.assert_not_called()
    mocked_atom.parse.assert_not_called()
