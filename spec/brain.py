from pretend import stub
"""
CosmoBot

    - it tweets with the paper title, authors, and link
"""
from cosmotweet.brain import CosmoBot
def test_CosmoBot_create_tweet():
    cosmobot = CosmoBot(
        tweet_maker=stub(make_tweet=lambda x: x),
        arxiv_daily=stub()
    )

    test_paper =  stub(
        title = 'Axion-Dilaton Destabilization and the Hubble Tension. (arXiv:1904.08912v1 [astro-ph.CO])',
        authors = 'Stephon Alexander, Evan McDonough',
        arxiv_id = '1904.08912',
        link = 'arxiv.org/abs/1904.08912',
        post_date = '2019-04-18T20:30:00-05:00'
    )

    test_tweet = cosmobot.create_tweet(test_paper)

    should_be = ('Axion-Dilaton Destabilization and the Hubble Tension.'
                 + '\n(Stephon Alexander, Evan McDonough).'
                 + '\narxiv.org/abs/1904.08912')

    assert should_be == test_tweet
