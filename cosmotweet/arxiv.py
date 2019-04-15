class Paper:
    pass

class ArxivDaily:
    def __init__(self, papers):
        self.papers = papers

    def get_papers(self, date):
        return {paper for paper in self.papers if paper.date == date}
