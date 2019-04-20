from cosmotweet.utils import get_rss_feed, strip_tags
from dataclasses import dataclass




@dataclass(eq=True, frozen=True)
class Paper:
    title: str
    authors: str
    arxiv_id: str
    link: str
    post_date: str


class ArxivDaily:
    def __init__(self, papers):
        self.papers = papers

    def get_papers(self, date):
        return set(paper for paper in self.papers if paper.date == date)


class ArxivRSS:
    def __init__(self):
        self.get_rss_feed = get_rss_feed


    def _get_author(self, auth_string):
        authors = strip_tags(auth_string)#.split(',')
        return authors #[auth.strip() for auth in authors]


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


    def retrieve_papers(self):
        URL = 'https://export.arxiv.org/rss/astro-ph.CO'
        rss_feed = self.get_rss_feed(URL)
        return rss_feed
