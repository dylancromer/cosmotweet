import random
from dataclasses import dataclass
from cosmotweet.utils import get_rss_feed, strip_tags



@dataclass(eq=True, frozen=True)
class Paper:
    title: str
    authors: str
    arxiv_id: str
    link: str
    post_date: str


class ArxivDaily:
    def __init__(self, papers):
        self.queue = set(random.sample(papers, len(sample)))

        self.times = self.construct_times()


    def construct_times(self):
        pass


class ArxivRSS:
    def __init__(self):
        self._get_rss_feed = get_rss_feed


    def fetch_feed(self):
        URL = 'https://export.arxiv.org/rss/astro-ph.CO'
        rss_feed = self._get_rss_feed(URL)
        return rss_feed


    def _get_author(self, auth_string):
        authors = strip_tags(auth_string)
        return authors


    def _get_id(self, id_string):
        if id_string.startswith('arxiv.org/abs/'):
            return id_string[14:]
        else:
            return id_string


    def _get_link(self, id_string):
        if id_string.startswith('http://'):
            return id_string[7:]
        else:
            return id_string


    def feed_to_papers(self, rss_feed):
        date = rss_feed['feed']['updated']

        titles = [title['title'] for title in rss_feed['entries']]

        raw_authors = [auths['authors'][0]['name'] for auths in rss_feed['entries']]
        authors = [self._get_author(auth) for auth in raw_authors]

        raw_ids = [id_['id'] for id_ in rss_feed['entries']]
        links = [self._get_link(id_) for id_ in raw_ids]
        ids = [self._get_id(link) for link in links]

        papers = set()
        for title,auth,id_,link in zip(titles, authors, ids, links):
            paper = Paper(title=title, authors=auth, arxiv_id=id_, link=link, post_date=date)
            papers.add(paper)

        return papers


    def fetch_current_papers(self):
        return self.feed_to_papers(self.fetch_feed())
