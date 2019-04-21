import time
import schedule
from cosmotweet.arxiv import ArxivDaily, ArxivRSS




def _get_current_day():
    #TODO: make less stupid
    return '2019-04-11'


def _get_current_time():
    #TODO: formatting may not be what I want
    return time.localtime()


class Cosmobot:
    def __init__(self):
        self.now = _get_current_time
        self.today = _get_current_day()

        self.arxiv_rss = ArxivRSS()
        current_papers = ArxivRSS.fetch_current_papers()

        self.arxiv_daily = ArxivDaily(current_papers)


    def _schedule(self):
        pass


    def create_tweet(self):
        pass


    def schedule_tweets(self):
        tweet_times = self.arxiv_daily.times
        papers_to_schedule = self.arxiv_daily.queue

        for time, paper in zip(tweet_times, papers_to_schedule):
            _schedule(self.create_tweet, arg=paper, time=time)


    def wait_to_refresh(self):
        self._schedule(self.refresh, time=self.arxiv_daily.refresh_time)
        self._sleep_until(self.arxiv_daily.refresh_time)


    def start_cycle(self):
        self.schedule_tweets()

        self.wait_to_refresh()


def test_Cosmobot():
    cosmobot = Cosmobot()
    cosmobot.start_cycle()
