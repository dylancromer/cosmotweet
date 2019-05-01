import time
from cosmotweet.scheduler import _schedule
from cosmotweet.arxiv import ArxivDaily, ArxivRSS
from cosmotweet.twitter import TweetMaker




class NoTweetMaker:
    pass


class NoArxivDaily:
    pass


class CosmoBot:
    def __init__(self, tweet_maker=NoTweetMaker(), arxiv_daily=NoArxivDaily()):
        self.arxiv_rss = ArxivRSS()

        if isinstance(arxiv_daily, NoArxivDaily):
            current_papers = self.arxiv_rss.fetch_current_papers()
            self.arxiv_daily = ArxivDaily(current_papers)
        else:
            self.arxiv_daily = arxiv_daily

        if isinstance(tweet_maker, NoTweetMaker):
            self.tweet_maker = TweetMaker()
        else:
            self.tweet_maker = tweet_maker


    def tweet_from_paper(self, paper):
        title = paper.title.split('.')[0] + '.'
        auth = '\n(' + paper.authors + ').'
        shortauth = '\n(' + paper.authors.split(',')[0] + ', et al).'
        link = '\n' + paper.link

        if len(title + auth + link) <= 280:
            tweet = title + auth + link
        elif len(title + shortauth + link) <= 280:
            tweet = title + shortauth + link
        else:
            used_chars = len(shortauth + link) + 3
            chars_left = 280 - used_chars
            tweet = title[:chars_left] + '...' + shortauth + link

        assert len(tweet) <= 280
        return tweet


    def create_tweet(self, paper):
        tweet = self.tweet_from_paper(paper)
        return self.tweet_maker.make_tweet(tweet)


    def _schedule_tweets(self):
        tweet_times = self.arxiv_daily.times
        papers_to_schedule = self.arxiv_daily.queue

        for time_, paper in zip(tweet_times, papers_to_schedule):
            _schedule(self.create_tweet, args=paper, wait_time=time_)


    def _wait_to_refresh(self):
        _schedule(self.refresh, time=self.arxiv_daily.refresh_time)
        self._sleep_until(self.arxiv_daily.refresh_time)


    def start_cycle(self):
        self._schedule_tweets()

        self.wait_to_refresh()
