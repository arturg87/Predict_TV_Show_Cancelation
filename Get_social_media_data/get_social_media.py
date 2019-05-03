from bs4 import BeautifulSoup
import urllib3
import json
import os
from os import path
import re 
import tweepy
import get_userprofileinfo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

baseDir = 'Predict_TV_Show_Cancelation'

twitter = get_userprofileinfo.searchTwitter()

def load_unparsed_json(whichJson):
    filename = whichJson + ".json"

    try:
        with open(os.path.join(baseDir, 'Data', filename), 'r') as f:
            return json.load(f)
    except:
        print("Could not load %s" %(filename))
        return None
    
#def getFacebookData(data):
    
def getTwitterData(searchQuery):
    return twitter.search(searchQuery)

def getMissing(data):
    socialMediaData = []
    for i in data: 
        if not i['official_sites']:
            # All social media data missing
            tweetData = getTwitterData(i['tv_show_name'])

            socialMediaData.append({
                'tv_show_name': i['tv_show_name'],
                'twitter_data': tweetData

            })
        else:
            testList = []
            for n in i['official_sites']: 
                testList.append([n['social_media_site'], n['social_media_link']])
                
            if "Official Facebook" not in testList[0]:
                # If Facebook data is missing
                pass
            if "Official Twitter" not in testList[0]:
                # If Twitter Data is missing
                tweetData = getTwitterData(i['tv_show_name'])
            if "Official Instagram" not in testList[0]:
                # If Instagram data is misisng
                pass

            socialMediaData.append({
                'tv_show_name': i['tv_show_name'],
                'twitter_data': tweetData

            })
                
    
    

rescuedData = load_unparsed_json("rescuedIMDB_Data")
canceledData = load_unparsed_json("canceledIMDB_Data")
renewedData = load_unparsed_json("renewedIMDB_Data")

test = getMissing(canceledData)
print(len(renewedData))