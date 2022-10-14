import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# Credentials
api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


class SoulectionTwitterBot:

    def __init__(self):
        self.client = tweepy.Client(consumer_key=api_key, consumer_secret=api_secret, access_token=access_token, access_token_secret=access_token_secret)
    
    def tweet(self, msg, id=None):
        tweet = self.client.create_tweet(text=msg, in_reply_to_tweet_id=id)
        return tweet
