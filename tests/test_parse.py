from xml.etree import ElementTree as etree
from datetime import date, timedelta
from lambdas import nea_download_feed


def test_is_recent():
    item_string = '<item><pubDate>{} 00:00:00</pubDate></item>'

    pub_date = date.today() - timedelta(days=3)
    pub_date_string = pub_date.strftime(nea_download_feed.pub_format)
    item = etree.fromstring(item_string.format(pub_date_string))
    assert nea_download_feed.is_recent(item) is True

    pub_date = date.today() - timedelta(days=17)
    pub_date_string = pub_date.strftime(nea_download_feed.pub_format)
    item = etree.fromstring(item_string.format(pub_date_string))
    assert nea_download_feed.is_recent(item) is False


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
    assert nea_download_feed.parse_item(item) == item_parameters


def test_parse_blog():
    recent_date = date.today() - timedelta(days=3)
    recent_date_string = recent_date.strftime(nea_download_feed.pub_format)

    older_date = date.today() - timedelta(days=17)
    older_date_string = older_date.strftime(nea_download_feed.pub_format)

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

    parsed = nea_download_feed.parse_blog(item_string)
    assert parsed['title'] == 'Blog Title'
    assert len(parsed['items']) == 2


def test_lambda_handler(monkeypatch):
    def mock_download_feed(url):
        return """
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
    with monkeypatch.context() as m:
        m.setattr(nea_download_feed, 'download_feed', mock_download_feed)

        event = {
            'urls': ['https://example.com/feed1', 'https://example.com/feed1']
        }

        assert len(nea_download_feed.lambda_handler(event, {})) == 2
