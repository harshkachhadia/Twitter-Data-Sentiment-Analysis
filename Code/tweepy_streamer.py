from tweepy.streaming import StreamListener #class helps us listen to tweets based on certain keywords and hashtags
from tweepy import OAuthHandler #class responsible for authentication using tokens
from tweepy import Stream 

from tweepy import API #Refer tweepy API documentation for more methods
from tweepy import Cursor

import twitter_credentials as cred

import numpy as np
import pandas as pd


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            return tweets

    def get_friend_list(self, num_friends):
        friend_list = [] 
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
            return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key=cred.CONSUMER_KEY, consumer_secret=cred.CONSUMER_SECRET)
        auth.set_access_token(cred.ACCESS_TOKEN, cred.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #This handles twitter authentication and the connection to the Twitter Streaming API.
        listener = TwitterListener(fetched_tweets_filename)
        stream = Stream(twitter_authenticator, listener)
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener): 
    """
    This is a basic listener class that just prints received tweets to stdout
    """    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, raw_data): #it will take in data from stream listener which is listening for tweets
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data)
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    
    def on_error(self, status_code): #method runs if error occurs and helps us print the status message
        if status_code == 420:
            #Returning False on data method in case rate limimt occurs
            return False
        print(status_code)

if __name__== "__main__":
    hash_tag_list = ['DOnald Trump', 'Hillary Clinton', 'Barack Obama', 'Bernie Sanders']
    fetched_tweets_filename = "tweets.json"

    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename=fetched_tweets_filename,hash_tag_list=hash_tag_list)
    twitter_client = TwitterClient('amanshah611')
    print(twitter_client.get_user_timeline_tweets(1))