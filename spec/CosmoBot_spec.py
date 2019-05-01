from pretend import stub
from cosmotweet.brain import CosmoBot
"""
CosmoBot

    - it tweets with the paper title, authors, and link
"""
cosmobot = CosmoBot(
    tweet_maker=stub(),
    arxiv_daily=stub()
)

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
