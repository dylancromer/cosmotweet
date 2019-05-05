import sys
from cosmotweet.arxiv import Paper
from cosmotweet.brain import CosmoBot
from pretend import stub

def main():
    cosmobot = CosmoBot()
    papers = {
        Paper(
            title = f'Axion-Dilaton Destabilization and the Hubble Tension. {i}',
            authors = 'Stephon Alexander, Evan McDonough',
            arxiv_id = '1904.08912',
            link = 'arxiv.org/abs/1904.08912',
            post_date = '2019-04-18T20:30:00-05:00'
        ) for i in range(20000)
    }

    cosmobot.arxiv_rss = stub(fetch_current_papers=lambda: papers)

    cosmobot.tweet_maker = stub(make_tweet=lambda tweet: sys.stdout.write(tweet))

    cosmobot.start_cycle()

if __name__ == '__main__':
    main()
