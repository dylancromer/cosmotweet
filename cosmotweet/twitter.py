import os
import os.path as pth
from dotenv import load_dotenv
import tweepy




class TweetMaker:
    def __init__(self):
        dotenv_path = pth.abspath(pth.join(pth.dirname(__file__), '..', '.env'))
        load_dotenv(dotenv_path)

        CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
        CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
        ACCESS_KEY = os.environ.get("ACCESS_KEY")
        ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

        self.api = tweepy.API(self.auth)


    def make_tweet(self, tweet):
        self.api.update_status(tweet)
