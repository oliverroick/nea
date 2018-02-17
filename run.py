
from nea import download, parser

feed_sources = []


if __name__ == "__main__":
    with open('feeds.txt') as feeds:
        feed_sources = download.get_feeds(feeds)

    news = (parser.parse_blog(feed) for feed in feed_sources)
