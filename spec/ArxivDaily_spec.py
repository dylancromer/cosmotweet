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

def test_times():
    times = daily.times

    assert len(times) == 3

    for time_ in times:
        assert time_ > 0
        assert time_ < daily.refresh_time

    assert sum(times) < 24*60*60

"""
    - the times are spaced semi-evenly until the next papers are posted
"""

def test_time_spacing():
   times = daily.times

   interval = daily.refresh_time/3
   min_interval = interval/2
   max_interval = 2*interval

   assert np.all(np.diff(times) > min_interval)
   assert np.all(np.diff(times) < max_interval)
