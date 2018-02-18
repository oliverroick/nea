from nea import download, parser, templates

if __name__ == "__main__":
    feed_sources = []
    with open('feeds.txt') as feeds:
        feed_sources = download.get_feeds(feeds)

    new_blogs = (parser.parse_blog(feed) for feed in feed_sources)
    mail = templates.render(new_blogs)
