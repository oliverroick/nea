from xml.etree import ElementTree as etree
from unittest.mock import patch
from lambdas import nea_get_blog


@patch('lambdas.nea_get_blog.parse_feed')
def test_lambda_handler(mocked_parse_feed, monkeypatch):
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
        mocked_parse_feed.parse.return_value = {'title': 'Blog Title'}

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

        mocked_parse_feed.assert_called_with(feed_rss)

        assert result['email_to'] == event['email_to']
        assert result['email_from'] == event['email_from']
        assert len(result['urls']) == 1
        assert len(result['blogs']) == 2

        mocked_parse_feed.reset_mock()
        event = {
            'email_to': 'john@example.com',
            'email_from': 'jane@example.com',
            'urls': [
                'https://example.com/feed1',
                'https://example.com/feed2'
            ]
        }

        result = nea_get_blog.lambda_handler(event, {})
        mocked_parse_feed.assert_called_with(feed_rss)

        assert result['email_to'] == event['email_to']
        assert result['email_from'] == event['email_from']
        assert len(result['urls']) == 1
        assert len(result['blogs']) == 1

        mocked_parse_feed.reset_mock()

        event = {
            'email_to': 'john@example.com',
            'email_from': 'jane@example.com',
            'urls': [
                'https://example.com/feed1'
            ]
        }

        result = nea_get_blog.lambda_handler(event, {})
        mocked_parse_feed.assert_called_with(feed_rss)

        assert result['email_to'] == event['email_to']
        assert result['email_from'] == event['email_from']
        assert result['urls'] == -1
        assert len(result['blogs']) == 1
