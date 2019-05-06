import urllib3
import json
import os
from os import path
import re 
import get_userprofileinfo
import update_social_media_links
from pandas.util.testing import network

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

baseDir = 'Predict_TV_Show_Cancelation'

twitter = get_userprofileinfo.searchTwitter()
handle = get_userprofileinfo.getURLData()
update = update_social_media_links.updateSMLink()

def load_unparsed_json(whichJson):
    # functions loads json data
    filename = whichJson + ".json"

    try:
        with open(os.path.join(baseDir, 'Data', filename), 'r') as f:
            return json.load(f)
    except:
        print("Could not load %s" %(filename))
        return None
    
def getNetworkList(data1, data2, data3):
    networks = []

    # combine all datasets into one large list 
    largeList = {x['tv_network']:x for x in data1+data2+data3}.values()

    # search through the large list and extract all networks
    for i in largeList:
        if i['tv_network'] is not None:
            networks.append(str(i['tv_network']).lower())

    # remove duplicate from large list
    networks = list(set(networks))

    # remove wierd egde case
    networks.remove('for a drama')
    
    return networks

def getMissing(data, networkList):
    socialMediaData = []
    cheatList = ['Zoo', 'Will', 'Hap and Leonard', 'The Quad']

    for i in data: 
        # if show is in the cheater list, add the network in the query for a better result
        if i['tv_show_name'] in cheatList:
            query = i['tv_show_name']+" "+i['tv_network'] 
        else:
            query = i['tv_show_name']

        # If an official site was never added in IMDB, search twitter for likely match
        if not i['official_sites']:
            # All social media data missing
            tweetData = twitter.search(query, str(i['tv_network']))

            socialMediaData.append({
                'tv_show_name': i['tv_show_name'],
                'twitter_data': tweetData
            })
        else:
            # If imdb data had official sites data

            testList = []

            for n in i['official_sites']: 
                testList.append({
                    'social_media_site': n['social_media_site'], 
                    'social_media_link': n['social_media_link']
                })

            # Iterate through each type of social media sites available from IMDb
            for typeSM in testList:
                # If site is Twitter, get more information
                if "Official Twitter" in typeSM['social_media_site']:
                    
                    # I noticed early that the external link in IMDb for social media side 
                    # have a changing token in its url, thus, I will get the most updated link.

                    # Get the IMDb link for the tv show
                    link = getShowLink(i['tv_show_name'])

                    # Get the most updated link for the IMDb has for Twitter
                    url = update.updateLinks(link, typeSM['social_media_site'])

                    # Pull the username from twitter
                    twitterUID = handle.getTwitterHandle(url)

                    if twitterUID == "Not Found":
                        # If the twitter page was not founc using the link from IMDb, 
                        # manually search twitter users for most likely user
                        tweetData = twitter.search(query, str(i['tv_network']))
                    else:    
                        # Use twitter api to get additional information
                        tweetData = twitter.search(twitterUID, str(i['tv_network']))
        
                    socialMediaData.append({
                        'tv_show_name': i['tv_show_name'],
                        'twitter_data': tweetData

                    })
    return socialMediaData

def getShowLink(searchName):
    # This function iterates through all data and looks for the show name that matches the define name
    # and return the shows link

    canceledLinks = load_unparsed_json("canceled")
    rescuedLinks = load_unparsed_json("rescued")
    renewedLinks = load_unparsed_json("renewed")
    
    # Combine all datasets into one
    largeList = {x['tv_show_imdb_link']:x for x in canceledLinks+rescuedLinks+renewedLinks}.values()

    # Iterate through all shows and look for the given show name
    for a in largeList: 
        for i in a['tv_show_name']:
            tester = str(i)
        #t1 = str(a['tv_show_name']).strip()
        #t2 = t1.replace(r'\\', '')
        #tester = re.sub(r'[\[\'][\'\]]','', str(a['tv_show_name']).strip())
        if tester == searchName:
            return a['tv_show_imdb_link']

def write_json(data, which_type):
        # filenames for specific list type
        if which_type == "renewed":
            filename = 'renewedTwitterData.json'
        elif which_type == "canceled":
            filename = 'canceledTwitterData.json'
        elif which_type == "rescued":
            filename = 'rescuedTwitterData.json'

        path = 'Predict_TV_Show_Cancelation//Data/'

        with open(os.path.join(path, filename), 'w') as outfile:
            outfile.write('[')
            outfile.write('\n')

            count = 1
            for i in data:
                json.dump(i, outfile)
                if count < len(data):
                    outfile.write(',\n')
                else:
                    outfile.write('\n')
                count+=1

            outfile.write(']')

# Load IMDb data
rescuedData = load_unparsed_json("rescued_IMDB_Data")
canceledData = load_unparsed_json("canceled_IMDB_Data")
renewedData = load_unparsed_json("renewed_IMDB_Data")

# get a list of networks
# may not be needed anymore
networkList = getNetworkList(rescuedData, canceledData, renewedData)

# get all twitter stats
rescuedTwitterStats = getMissing(rescuedData, networkList)
canceledTwitterStats = getMissing(canceledData, networkList)
renewedTwitterStats = getMissing(renewedData, networkList)

write_json(rescuedTwitterStats, "rescued")
write_json(canceledTwitterStats, "canceled")
write_json(renewedTwitterStats, "renewed")

print("Collection Complete")