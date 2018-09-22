from xml.etree import ElementTree as etree
from datetime import date, timedelta
from lambdas import nea_get_blog


def test_is_recent():
    item_string = '<item><pubDate>{} 00:00:00</pubDate></item>'

    pub_date = date.today() - timedelta(days=3)
    pub_date_string = pub_date.strftime(nea_get_blog.pub_format)
    item = etree.fromstring(item_string.format(pub_date_string))
    assert nea_get_blog.is_recent(item) is True

    pub_date = date.today() - timedelta(days=17)
    pub_date_string = pub_date.strftime(nea_get_blog.pub_format)
    item = etree.fromstring(item_string.format(pub_date_string))
    assert nea_get_blog.is_recent(item) is False


def test_parse_item():
    item_parameters = {
        'title': 'Some title',
        'link': 'http://example.com'
    }
    item_string = """
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <pubDate>Mon, 17 Sep 2018 00:00:00</pubDate>
            <description>Lots of words</description>
        </item>
    """
    item = etree.fromstring(item_string.format(**item_parameters))
    assert nea_get_blog.parse_item(item) == item_parameters


def test_parse_blog():
    recent_date = date.today() - timedelta(days=3)
    recent_date_string = recent_date.strftime(nea_get_blog.pub_format)

    older_date = date.today() - timedelta(days=17)
    older_date_string = older_date.strftime(nea_get_blog.pub_format)

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

    parsed = nea_get_blog.parse_blog(item_string)
    assert parsed['title'] == 'Blog Title'
    assert len(parsed['items']) == 2


def test_lambda_handler(monkeypatch):
    feed_rss = """
            <rss>
                <channel>
                    <title>Blog Title</title>
                    <item>
                        <title>Title</title>
                        <link>http://example.com</link>
                        <pubDate>Mon, 17 Sep 2018 00:00:00 +0000</pubDate>
                        <description>Lots of words</description>
                    </item>
                </channel>
            </rss>
        """

    def mock_download_feed(url):
        return feed_rss

    with monkeypatch.context() as m:
        m.setattr(nea_get_blog, 'download_feed', mock_download_feed)

        event = {
            'email_to': 'john@example.com',
            'email_from': 'jane@example.com',
            'urls': [
                'https://example.com/feed1',
                'https://example.com/feed2'
            ],
            'blogs': [{'title': 'Some blog'}],
        }

        result = nea_get_blog.lambda_handler(event, {})
        assert result['email_to'] == event['email_to']
        assert result['email_from'] == event['email_from']
        assert len(result['urls']) == 1
        assert len(result['blogs']) == 2

        event = {
            'email_to': 'john@example.com',
            'email_from': 'jane@example.com',
            'urls': [
                'https://example.com/feed1',
                'https://example.com/feed2'
            ]
        }

        result = nea_get_blog.lambda_handler(event, {})
        assert result['email_to'] == event['email_to']
        assert result['email_from'] == event['email_from']
        assert len(result['urls']) == 1
        assert len(result['blogs']) == 1

        event = {
            'email_to': 'john@example.com',
            'email_from': 'jane@example.com',
            'urls': [
                'https://example.com/feed1'
            ]
        }

        result = nea_get_blog.lambda_handler(event, {})
        assert result['email_to'] == event['email_to']
        assert result['email_from'] == event['email_from']
        assert result['urls'] == -1
        assert len(result['blogs']) == 1
