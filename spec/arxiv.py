from pretend import stub
"""
ArXivDaily

    get_papers

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
