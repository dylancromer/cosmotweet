import sys
from cosmotweet.arxiv import Paper
from cosmotweet.brain import CosmoBot
from pretend import stub


def test_main(mocker):
    papers = {
        Paper(
            title = f'Axion-Dilaton Destabilization and the Hubble Tension. {i}',
            authors = 'Stephon Alexander, Evan McDonough',
            arxiv_id = '1904.08912',
            link = 'arxiv.org/abs/1904.08912',
            post_date = '2019-04-18T20:30:00-05:00'
        ) for i in range(1360)
    }

    class FakeArxivRSS:
        def fetch_current_papers(self):
            return papers

    class FakeTweetMaker:
        def make_tweet(self, tweet):
            print(tweet)


    mocker.patch('cosmotweet.brain.ArxivRSS', new=FakeArxivRSS)
    mocker.patch('cosmotweet.brain.TweetMaker', new=FakeTweetMaker)

    cosmobot = CosmoBot()
    cosmobot.start_cycle()
