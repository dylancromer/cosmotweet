from pretend import stub
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

    retrieve_papers()

        - it returns all papers it can get from the arxiv RSS feed
"""
from cosmotweet.arxiv import ArxivRSS
def test_ArxivRSS_retrieve_papers():
    test_papers = {
        stub(date='2019-04-11T20:30:00-05:00'),
        stub(date='2019-04-11T20:30:00-05:00'),
        stub(date='2019-04-9T20:30:00-05:00')
    }

    arxiv_rss = ArxivRSS()
    arxiv_rss.get_rss_feed = lambda url : test_papers

    new_papers = arxiv_rss.retrieve_papers()

    assert new_papers == test_papers

"""
    feed_to_papers()

        - it returns a set of Papers given an RSS feed
"""
def test_ArxivRSS_feed_to_papers():
    test_feed = {
        'feed': {'title': 'astro-ph.CO updates on arXiv.org',
        'updated': '2019-04-14T20:30:00-05:00',
        'updated_parsed': time.struct_time(tm_year=2019, tm_mon=4, tm_mday=15, tm_hour=1, tm_min=30, tm_sec=0, tm_wday=0, tm_yday=105, tm_isdst=0),
        'sy_updatebase': '1901-01-01T00:00+00:00'}
        'entries': [{'id': 'http://arxiv.org/abs/1904.05904',
        'title': 'the title'
        'links': [{'rel': 'alternate',
        'type': 'text/html',
        'href': 'http://arxiv.org/abs/1904.05904'}],
        'link': 'http://arxiv.org/abs/1904.05904',
        'summary': 'this is the abstract',
        'authors': [{'name': 'names of authors'}]}]
    }
