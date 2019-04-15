import time
import schedule
from cosmotweet.arxiv import ArxivDaily

def time_linspace(start, stop, num):
    pass

def _get_papers(date):
    pass

def _get_next_refresh_time(date):
    pass

class Cosmobot:
    def _schedule(self):
        pass

    def create_tweet(self):
        pass

    def establish_daily_queue(self):
        self.next_arxiv_refresh_time = _get_next_refresh_time(self.today)

        self.paper_queue = _get_papers(self.today)

    def schedule_tweets(self):
        tweet_times = time_linspace(self.now, self.next_arxiv_refresh_time, len(self.paper_queue))

        for time,paper in zip(tweet_times, self.paper_queue):
            _schedule(self.create_tweet, arg=paper, time=time)

    def wait_to_refresh(self):
        _schedule(self.refresh, time=time)

    def start_cycle(self):
        self.establish_daily_queue()

        self.schedule_tweets()

        self.wait_to_refresh()

#logic looks like
#   start()
#   establish_daily_queue()
#   create some frequency sufficient to tweet out all papers before the next ones come
#
#   tweet_times = arange(now, refresh_time, num_papers)
#   papers = randomize(queue.papers)
#   for time,paper in tweet_times,papers:
#       schedule create_tweet(paper) @ time
#
#   when thetime is current:
#       refresh()

