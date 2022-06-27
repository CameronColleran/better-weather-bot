from dataclasses import dataclass
import re
from readline import get_endidx
from webbrowser import get
import tweepy
import config
import requests

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
@dataclass
class Weather:
    temp: str
    description: str
    humidity: str

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
    most_recent_id = get_last_tweet_id(config.PREV_TWEET_ID_FILENAME)
    if most_recent_id != '': # no tweets yet
        mentions = api.mentions_timeline(since_id = get_last_tweet_id(config.PREV_TWEET_ID_FILENAME))
    else:
        mentions = api.mentions_timeline()
    return reversed(mentions)

def respond_to_mention(mention):
    # TODO: add more robust string parsing (i.e. get the city from a 'City, State' format)
    location = (re.sub('@[\w]+', '', mention.text)).strip() 
    print(location)
    id = mention.id
    set_last_tweet_id(id, config.PREV_TWEET_ID_FILENAME)
    weather = get_weather(location)
    if weather == None:
        weather_message = 'Sorry, I\'m not familiar with that city! Make sure your tweet is formatted with just the city name after your mention (i.e. New York)'
    else:
        # TODO: add more information to the message
        weather_message = f'Currently {str(weather.temp)}°F in {location} with a humidity of {weather.humidity}% and {weather.description}'
    api.update_status(status = weather_message, in_reply_to_status_id = id, auto_populate_reply_metadata = True)

def get_weather(city_name):
    request_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={config.OPEN_WEATHER_API_KEY}'
    response = requests.get(request_url).json()
    try:
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        humiditiy = response['main']['humidity']
        output = Weather(temp=temp, description=desc, humidity=humiditiy)
        return output
    except:
        return None