#http://stackoverflow.com/questions/24163421/twitter-user-profile-can-be-extracted-by-this

import tweepy
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

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
        self.count = 0

    def search(self, query, network, networkList=[]):
        
        print(str(self.count) + " "+ query)
        self.count =+ self.count + 1

        temp_data = []

        api = tweepy.API(auth)
        #twitterStream = Stream(auth,TweetListener())

        try:
            users = api.search_users(query)
            weight = 0
            tempWeight = 0

            for i in users:

                # get users verified status, name, screen name, and description
                isVerified = i.verified
                name = i.name
                screenName = i.screen_name
                description = i.description
                
                # remove any non-alphanumeric characters
                queryTest = re.sub(r'[^a-zA-Z0-9\s]', '', query)
                nameTest = re.sub(r'[^a-zA-Z0-9\s]', '', name)
                desc = re.sub(r'[^a-zA-Z0-9\s]', '', description)
                netTest = re.sub(r'[^a-zA-Z0-9\s]', '', network)    

                # setup a series of checks we can use as a crude algorithm at determine the likelyhood of finding the correct twitter user. 
                 
                # Check if any part of the twitter name and the query name are equal 
                check1 = (queryTest in nameTest) or (nameTest in queryTest)

                # Check to see if the word Official shows up in the description
                check2 = ("official" in description.lower())
            
                # Check to see if the shows network (abc, cbs, etc...) is in the description
                check3 = netTest.lower() in desc.lower()

                # Check to see if the shows network (abc, cbs, etc...) is in the name
                check4 = netTest.lower() in nameTest.lower()

                # Check to see if the name and the query matches exactly with or with spaces (The Rise vs TheRise)
                check5 = (nameTest == queryTest) or (nameTest == re.sub(' ', '', queryTest))

                # Check to see if the screenname and query matches exactly
                check6 = query == screenName

                # Arbitrarily added value to the check I found to be most important
                # Also, if the user is verified, I added additional weight
                if check1 and check2 and (check3 or check4):
                    weight = 1
                    if isVerified: weight=weight*2
                elif check6:
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
                elif check5 and (check3 or check4):
                    weight = 0.5
                    if isVerified: weight=weight*2
                elif check5:
                    weight = 0.4
                    if isVerified: weight=weight*2
                elif check4 and check3:
                    weight = 0.3
                    if isVerified: weight=weight*2

                # Keep track of the highest weight and set the data accordingly
                if weight > tempWeight:
                    tempWeight = weight

                    temp_data = {
                        'name':i.name, 
                        'screen_name': i.screen_name,
                        'followers_count':i.followers_count
                    }  
                    
                    # If max weight, no need to continue looping through twiiter users, break the loop and return the data
                    if weight == 2:
                        break  

            if not temp_data:
                temp_data = None

            return temp_data   
                
        except Exception as e:
            print(e)
            pass

class getURLData():

    def getTwitterHandle(self, url):
        # function gets the twitter handle from the passed in url

        http = urllib3.PoolManager()
        fp = http.request('GET', url)
        soup = BeautifulSoup(fp.data, features='lxml')
        
        try:
            twitterHandle = soup.find('b', {'class':'u-linkComplex-target'}).text
        except:
            twitterHandle = "Not Found"
        
        return twitterHandle




        