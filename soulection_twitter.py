###################################################################
###### Setting up twitter bot to release playlist information
###### gxrsha
###################################################################

import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# client = tweepy.Client(consumer_key=os.getenv('TWITTER_API_KEY'), consumer_secret=os.getenv('TWITTER_API_SECRET'), access_token=os.getenv('TWITTER_ACCESS_TOKEN'), access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'))
auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN_'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)
client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'), consumer_key=os.getenv('TWITTER_API_KEY'), consumer_secret=os.getenv('TWITTER_API_SECRET'), access_token=os.getenv('TWITTER_ACCESS_TOKEN'), access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

print('Connected to twitter..')


def create_tweet():
    client.create_tweet(text="Hello")
