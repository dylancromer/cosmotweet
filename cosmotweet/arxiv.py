from cosmotweet.utils import get_rss_feed

class Paper:
    pass

class ArxivDaily:
    def __init__(self, papers):
        self.papers = papers

    def get_papers(self, date):
        return {paper for paper in self.papers if paper.date == date}

class ArxivRSS:
    def __init__(self):
        self.get_rss_feed = get_rss_feed

    def feed_to_papers(self, rss_feed):
        pass

    def retrieve_papers(self):
        URL = 'https://export.arxiv.org/rss/astro-ph.CO'
        rss_feed = self.get_rss_feed(URL)
        return rss_feed
