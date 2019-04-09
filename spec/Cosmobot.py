import time
import pytest
from pretend import stub

'''
COSMOBOT: Class

    - it periodically checks for new content from astro-ph.CO
'''
class ArxivPaper:
    pass

from cosmotweet.brain import Cosmobot

def test_Cosmobot_updates_when_arxiver_updates():
    arxiv_paper_1 = ArxivPaper()
    arxiver = stub(feed={arxiv_paper_1})

    cosmobot = Cosmobot(arxiver)

    assert cosmobot.arxiver.feed == {arxiv_paper_1}

    arxiv_paper_2 = ArxivPaper()
    arxiver.feed.add(arxiv_paper_2)

    assert cosmobot.arxiver.feed == {arxiv_paper_1, arxiv_paper_2}
'''
    - it has a queue of content to be tweeted for the day
    - it tweets at intervals during the day all of the papers posted the evening before
'''
