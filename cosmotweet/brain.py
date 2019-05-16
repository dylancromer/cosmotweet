import time
from cosmotweet.arxiv import ArxivDaily, ArxivRSS
from cosmotweet.twitter import TweetMaker
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt




class CosmoBot:
    def update_feed(self):
        self.arxiv_rss = ArxivRSS()
        current_papers = self.arxiv_rss.fetch_current_papers()
        self.arxiv_daily = ArxivDaily(current_papers)

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

        try:
            return self.tweet_maker.make_tweet(tweet)
        except AttributeError:
            self.tweet_maker = TweetMaker()
            return self.tweet_maker.make_tweet(tweet)

    def _schedule(self, func, args, wait_time):
        scheduled_time = self.start_time + dt.timedelta(seconds=wait_time)
        try:
            self.scheduler.add_job(func, 'date', run_date=scheduled_time, args=(args,))
        except AttributeError:
            self.scheduler = BackgroundScheduler()
            self.scheduler.start()
            self.scheduler.add_job(func, 'date', run_date=scheduled_time, args=(args,))

    def _schedule_tweets(self):
        self.update_feed()
        self.start_time = dt.datetime.now()

        tweet_times = self.arxiv_daily.get_times()
        papers_to_schedule = self.arxiv_daily.get_random_queue()

        for time_, paper in zip(tweet_times, papers_to_schedule):
            self._schedule(self.create_tweet, args=paper, wait_time=time_)

    def reset_scheduler(self):
        self.scheduler.shutdown()

    def refresh(self):
        self.reset_scheduler()
        return self.start_cycle()

    def start_cycle(self):
        self._schedule_tweets()

        refresh_time =  self.arxiv_daily.get_update_time()
        time.sleep(refresh_time)
        return self.refresh()
