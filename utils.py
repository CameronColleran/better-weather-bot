import re
import tweepy
import config

def get_last_tweet_id(file):
    with open(file, 'r') as openfile:
        id = openfile.read()    
    if id == '':
        return ''
    id = int(id.strip())
    return id

def set_last_tweet_id(id, file):
    f_write = open(file, 'w')
    f_write.write(str(id))
    f_write.close()


def get_mentions():
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    # DEV_NOTE: first tweet id is 1540852511149461505 for testing purposes  
    most_recent_id = get_last_tweet_id(config.PREV_TWEET_ID_FILENAME)
    if most_recent_id != '': # no tweets yet
        mentions = api.mentions_timeline(since_id = get_last_tweet_id(config.PREV_TWEET_ID_FILENAME))
    else:
        mentions = api.mentions_timeline()
    return reversed(mentions)

def respond_to_mention(mention):
    location = (re.sub('@[\w]+', '', mention.text)).strip() 
    print(location)
    id = mention.id
    set_last_tweet_id(id, config.PREV_TWEET_ID_FILENAME)
    # TODO: add response