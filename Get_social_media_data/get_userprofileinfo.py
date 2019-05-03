#http://stackoverflow.com/questions/24163421/twitter-user-profile-can-be-extracted-by-this

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import csv
import re

consumer_key = 'KWSG911c1t2slxM0ysHylizZV'
consumer_secret = 'NHNBsv6lBh2SwWOFgqEUuzs3vRQOJA6DTXcD54SQFvACp7aV16'
access_key = '1087829569871269888-nNy14teT6gakLKeE5e06xTvcQxneyX'
access_secret = 'l77C3MVGBygegvLMGmtkNMd08g0nxcozB8oJY8mISDd21'

auth = OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
auth.set_access_token(access_key, access_secret)

class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)
#search

class searchTwitter():
    def __init__(self):
        self.twitter_data = []

    def search(self, query):

        api = tweepy.API(auth)
        twitterStream = Stream(auth,TweetListener())

        print(query)
        try:
            users = api.search_users(query)
            networkList = ['abc', 'nbc', 'cbs', 'fox', 'netflix', 'cw', 'usa', 'comedy central', 'spike', 'starz']
            weight = 0
            tempWeight = 0

            for i in users:
                isVerified = i.verified
                name = i.name
                description = i.description
                
                queryTest = re.sub('[^a-zA-Z0-9\s]', '', query)
                nameTest = re.sub('[^a-zA-Z0-9\s]', '', name)

                check1 = (queryTest in nameTest) or (nameTest in queryTest)
                check2 = ("official" in description.lower())
                check3 = any(net in description.lower() for net in networkList)
                check4 = any(net in name.lower() for net in networkList)
                
                if check1 and check2 and (check3 or check4):
                    weight = 1
                    if isVerified: weight=weight*2
                elif check1 and (check3 or check4):
                    weight = 0.8
                    if isVerified: weight=weight*2
                elif check1 and check2:
                    weight = 0.75
                    if isVerified: weight=weight*2
                elif check1 and check2:
                    weight = 0.6
                    if isVerified: weight=weight*2
                elif check2:
                    weight = 0.5
                    if isVerified: weight=weight*2
                elif (check3 or check4):
                    weight = 0.5
                    if isVerified: weight=weight*2
                elif check1:
                    weight = 0.25
                    if isVerified: weight=weight*2

                if weight > tempWeight:
                    tempWeight = weight

                    temp_data = {
                        'name':i.name, 
                        'screen_name': i.screen_name,
                        'followers_count':i.followers_count
                    }      

            return temp_data   
                #bool3 = any(string in description for string.lower() in networkList)
                #if check1 and check2 and (check3 or check4):
                #    tweetData = {
                #        'name':i.name, 
                #        'screen_name': i.screen_name,
                #        'followers_count':i.followers_count
                #    }
                #    print(i.name)
                #    return tweetData
        except Exception as e:
            print(e)
            pass
