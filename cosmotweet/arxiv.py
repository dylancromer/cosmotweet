import random
import datetime
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
        self.papers = papers
        self.POST_TIME = datetime.time(hour=20, minute=45)
        self.now = datetime.datetime.now()


    def get_random_queue(self):
        return set(random.sample(papers, len(papers)))


    def _next_posting_day(self, now):
        today = now.weekday()

        assert 0 <= today <= 6

        if (today != 3) and (today != 4): #i.e. it's not Thursday or Friday
           return now + datetime.timedelta(days=1)

        elif today == 3:
           return now + datetime.timedelta(days=3)

        elif today == 4:
           return now + datetime.timedelta(days=2)


    def _feed_not_already_posted(self, now):
        today = now.weekday()

        if (today != 4) and (today != 5): #i.e. it's not Friday or Saturday
            todays_post_time = now.replace(hour=self.POST_TIME.hour,
                                           minute=self.POST_TIME.minute)
            return now < todays_post_time

        else:
            return False


    def get_update_time(self):
        now = self.now
        next_posting_day = self._next_posting_day(now)

        today = now.weekday()
        tomorrow = (now + datetime.timedelta(days=1)).weekday()

        if self._feed_not_already_posted(now):
            post_datetime = now.replace(
                hour=self.POST_TIME.hour,
                minute=self.POST_TIME.minute
            )

        else:
            post_datetime = next_posting_day.replace(
                hour=self.POST_TIME.hour,
                minute=self.POST_TIME.minute
            )

        update_time = post_datetime - now
        return update_time.total_seconds()


    def get_times(self):
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
