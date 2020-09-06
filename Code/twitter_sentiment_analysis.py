from tweepy import OAuthHandler 

from tweepy import API 

import numpy as np
import pandas as pd  
import matplotlib.pyplot as plt

from textblob import TextBlob
import re

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

ID = "" #Twitter ID of the account for which sentiment analysis has to be done
NoOfTweets = 20 #Mention number of tweets(strting from most recent) of account mentioned above to be utilized for sentiment analysis

class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


class TweetAnalyzer():
    """
    functionality for analyzing and categorizing content from tweets
    """

    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"    
        else:
            return "negative"   

    def tweets_to_data_frame (self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

if __name__== "__main__":
    twitter_client = TwitterClient() 
    tweet_analyzer = TweetAnalyzer()
    
    api = twitter_client.twitter_client
    tweets = api.user_timeline(id=ID, count=NoOfTweets)
    
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    print(df['sentiment'].head(10))




#print(dir(tweets[0]))


#Simple data analysis on received twitter data
##################################################################################

#Get average length over all tweets.
    #print(np.mean(df['len']))
#Get the number of retweets for most retweeted tweet.
    #print(np.max(df['retweets']))
#Get the number of likes for most liked tweet.
    #print(np.max(df['likes']))

#Time Series Analysis
##################################################################################
#Time Series plot between likes vs date   
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16,4), color='r')
    # #plt.show()

#Time Series plot between retweets vs date
    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16,4), color='r')
    # plt.show()
    
#Time Series plot between likes,retweets vs date both in one plot    
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16,4), label='likes', legend=True)
    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16,4), label='retweets', legend=True)
    # plt.show()

###################################################################################
