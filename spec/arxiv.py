from pretend import stub
import time
"""
ArXivDaily

    get_papers(date)

        - it returns the papers for the day, but not those from the day before
"""
from cosmotweet.arxiv import ArxivDaily
def test_ArxivDaily_papers():
    date = '2019-04-11T20:30:00-05:00'
    paper1 = stub(title='Making amazing new cosmologies with Walruses and the Cheese Group', date='2019-04-11T20:30:00-05:00')
    paper2 = stub(title='Cosmology is Great, and You Should Give Cosmologists Money', date='2019-04-10T20:30:00-05:00')
    test_papers = {paper1, paper2}

    arxiv_papers = ArxivDaily(papers=test_papers)

    assert arxiv_papers.get_papers(date) == {paper1}

"""
ArxivRSS

    fetch_feed()

        - it returns all papers it can get from the arxiv RSS feed
"""
from cosmotweet.arxiv import ArxivRSS
def test_ArxivRSS_fetch_feed():
    test_papers = {
        stub(date='2019-04-11T20:30:00-05:00'),
        stub(date='2019-04-11T20:30:00-05:00'),
        stub(date='2019-04-9T20:30:00-05:00')
    }

    arxiv_rss = ArxivRSS()
    arxiv_rss.get_rss_feed = lambda url : test_papers

    new_papers = arxiv_rss.fetch_feed()

    assert new_papers == test_papers

"""
    feed_to_papers()

        - it returns a set of Papers given an RSS feed
"""
import pickle
from cosmotweet.arxiv import Paper
def test_ArxivRSS_feed_to_papers():
    with open('data/test/test_rss.pkl', 'rb') as pickle_file:
        rss_test = pickle.load(pickle_file)

    papers = ArxivRSS().feed_to_papers(rss_test)

    should_be = Paper(
        title = 'Axion-Dilaton Destabilization and the Hubble Tension. (arXiv:1904.08912v1 [astro-ph.CO])',
        authors = 'Stephon Alexander, Evan McDonough',
        arxiv_id = '1904.08912',
        link = 'arxiv.org/abs/1904.08912',
        post_date = '2019-04-18T20:30:00-05:00'
    )

    assert should_be in papers

"""
    fetch_current_papers()

        - it returns a set of the current papers
"""
def test_ArxivRSS_fetch_current_papers():
    with open('data/test/test_rss.pkl', 'rb') as pickle_file:
        rss_test = pickle.load(pickle_file)

    arxiv_rss = ArxivRSS()
    arxiv_rss.fetch_feed = lambda : rss_test

    papers = arxiv_rss.fetch_current_papers()

    should_be = Paper(
        title = 'Axion-Dilaton Destabilization and the Hubble Tension. (arXiv:1904.08912v1 [astro-ph.CO])',
        authors = 'Stephon Alexander, Evan McDonough',
        arxiv_id = '1904.08912',
        link = 'arxiv.org/abs/1904.08912',
        post_date = '2019-04-18T20:30:00-05:00'
    )

    assert should_be in papers
