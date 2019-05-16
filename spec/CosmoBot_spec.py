import time
import datetime as dt
from pretend import stub
from cosmotweet.brain import CosmoBot
"""
CosmoBot

    - it tweets with the paper title, authors, and link
"""
cosmobot = CosmoBot()

def test_CosmoBot_tweet_from_paper():

    test_paper =  stub(
        title = 'Axion-Dilaton Destabilization and the Hubble Tension. (arXiv:1904.08912v1 [astro-ph.CO])',
        authors = 'Stephon Alexander, Evan McDonough',
        arxiv_id = '1904.08912',
        link = 'arxiv.org/abs/1904.08912',
        post_date = '2019-04-18T20:30:00-05:00'
    )

    test_tweet = cosmobot.tweet_from_paper(test_paper)

    should_be = ('Axion-Dilaton Destabilization and the Hubble Tension.'
                 + '\n(Stephon Alexander, Evan McDonough).'
                 + '\narxiv.org/abs/1904.08912')

    assert should_be == test_tweet

"""
    - it won't try to make a tweet longer than 280 chars
"""
def test_CosmoBot_tweet_from_paper_too_long():
    test_paper = stub(
        title = 'Axion-Dilaton and ' + 280*'e',
        authors = ('Brady Haran, CGP Grey, Duke of Venezuela'),
        arxiv_id = '1904.08912',
        link = 'arxiv.org/abs/1904.08912',
        post_date = '2019-04-18T20:30:00-05:00'
    )

    test_tweet = cosmobot.tweet_from_paper(test_paper)

    should_be = ('Axion-Dilaton and ' + 212*'e' + '...'
                 + '\n(Brady Haran, et al).'
                 + '\narxiv.org/abs/1904.08912')

    assert should_be == test_tweet
    assert len(test_tweet) == 280

"""
    - it can schedule a task to be done later
"""
def test_CosmoBot__schedule():
    test_object = stub(soul='A very good soul')

    def testfunc(obj):
        obj.soul = 'A naughty soul'

    args = (test_object, )
    time_ = 0.01

    cosmobot.start_time = dt.datetime.now()
    cosmobot._schedule(testfunc, args, time_)

    assert test_object.soul == 'A very good soul'
    time.sleep(time_)
    assert test_object.soul == 'A naughty soul'
