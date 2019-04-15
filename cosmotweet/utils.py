import feedparser

def get_rss_feed(url):
    return feedparser.parse(url)
