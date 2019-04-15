import time
import schedule
from cosmotweet.arxiv import ArxivDaily, ArxivRSS

def time_linspace(start, stop, num):
    pass

def _get_current_day():
    return '2019-04-11'

def _get_current_time():
    return time.localtime()

class Cosmobot:
    def _get_papers(self, date):
        return self.arxiv_daily.papers(date)

    def _get_next_refresh_time(self, date):
        pass

    def __init__(self):
        self.now = _get_current_time
        self.today = _get_current_day()

        self.arxiv_rss = ArxivRSS()
        current_papers = ArxivRSS.retrieve_papers()

        self.arxiv_daily = ArxivDaily(current_papers)

    def _schedule(self):
        pass

    def create_tweet(self):
        pass

    def establish_daily_queue(self):
        self.next_arxiv_refresh_time = _get_next_refresh_time(self.today)

        self.paper_queue = _get_papers(self.today)

    def schedule_tweets(self):
        tweet_times = time_linspace(self.now(), self.next_arxiv_refresh_time, len(self.paper_queue))

        for time,paper in zip(tweet_times, self.paper_queue):
            _schedule(self.create_tweet, arg=paper, time=time)

    def wait_to_refresh(self):
        _schedule(self.refresh, time=time)

    def start_cycle(self):
        self.establish_daily_queue()

        self.schedule_tweets()

        self.wait_to_refresh()

def test_Cosmobot():
    cosmobot = Cosmobot()
    cosmobot.start_cycle()
