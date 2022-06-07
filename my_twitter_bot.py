import tweepy
import config

auth = tweepy.OAuth1UserHandler(
   config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET
)