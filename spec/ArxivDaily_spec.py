import datetime as dt
import numpy as np
from pretend import stub
from cosmotweet.arxiv import ArxivDaily
"""
ArXivDaily

    - it computes the times to tweet papers at
"""

papers = {
    stub(title='Amazing Paper #1'),
    stub(title='Amazing Paper #2'),
    stub(title='Amazing Paper #3')
}

daily = ArxivDaily(papers)
daily.today = 'monday'

def _times():
    times = daily.times

    assert len(times) == 3

    for time_ in times:
        assert time_ > 0
        assert time_ < daily.refresh_time

    assert sum(times) < 24*60*60

"""
    - the times are spaced semi-evenly until the next papers are posted
"""

def _time_spacing():
   times = daily.times

   interval = daily.refresh_time/3
   min_interval = interval/2
   max_interval = 2*interval

   assert np.all(np.diff(times) > min_interval)
   assert np.all(np.diff(times) < max_interval)

"""
    - the refresh time is always the next day ArXiv will update it's feed
"""

def test_next_posting_day():
    now = dt.datetime(2019, 5, 4, 17, 1, 24, 227761)

    test_times = [now]
    for i in range(1,6):
        test_times.append(now + dt.timedelta(days=i))

    should_bes = [
        now + dt.timedelta(days=1), #SAT
        now + dt.timedelta(days=2), #SUN
        now + dt.timedelta(days=3), #MON
        now + dt.timedelta(days=4), #TUE
        now + dt.timedelta(days=5), #WED
        now + dt.timedelta(days=8), #THU
        now + dt.timedelta(days=8), #FRI
    ]

    for time_,should_be in zip(test_times, should_bes):
        assert should_be == daily._next_posting_day(time_)

"""
    - it knows when the feed has already been posted for the day
"""

def test_feed_not_already_posted():
    time_before_post = dt.datetime(2019, 5, 2, 12, 0, 0, 0)
    assert daily._feed_not_already_posted(time_before_post)

"""
    - it knows when the feed has not already been posted for the day
"""

def test_feed_already_posted():
    base_time = dt.datetime(2019, 5, 2, 23, 30, 0, 0)

    for i in range(7):
        time_after_11 = base_time + dt.timedelta(days=i)
        assert not daily._feed_not_already_posted(time_after_11)

    time_on_a_friday_before_11 = dt.datetime(2019, 5, 10, 3, 0, 0, 0)
    assert not daily._feed_not_already_posted(time_on_a_friday_before_11)

    time_on_a_saturday_before_11 = dt.datetime(2019, 5, 4, 3, 0, 0, 0)
    assert not daily._feed_not_already_posted(time_on_a_saturday_before_11)

"""
    - the refresh time is always the next posting day at 8:30
"""

def test_update_time_weekday():
    daily._get_current_time = lambda: dt.datetime(2019, 5, 1, 23, 1, 0, 0)
    update_time = daily.get_update_time()
    should_be = 23*(60**2) + 59*60
    assert should_be == update_time

    daily._get_current_time = lambda: dt.datetime(2019, 5, 1, 22, 59, 0, 0)
    update_time = daily.get_update_time()
    should_be = 60
    assert should_be == update_time

def test_update_time_weekend():
    daily._get_current_time = lambda: dt.datetime(2019, 5, 3, 13, 0, 0, 0)
    update_time = daily.get_update_time()
    should_be = 2*24*(60**2) + 10*(60**2)
    assert should_be == update_time

"""
    - it computes times to post papers, with random noise
"""

def test_get_times():
    daily._get_current_time = dt.datetime.now
    now = daily._get_current_time()
    update_time = daily.get_update_time()

    tweet_times = daily.get_times()
    for tweet_time in tweet_times:
        assert tweet_time > 0
        assert tweet_time < update_time
