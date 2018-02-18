import os
from nea import download, parser, templates, mail

if __name__ == "__main__":
    feed_sources = []
    with open(os.environ.get('FEEDS'), 'feeds.txt') as feeds:
        feed_sources = download.get_feeds(feeds)

    new_blogs = (parser.parse_blog(feed) for feed in feed_sources)
    content = templates.render(new_blogs)

    if content:
        mail.send_mail(content)
