#%% [markdown]
## Predicting the renewal or cancelation of TV shows

#### By: Artur Gregorian
##### On my honor, as a student, I have neither received nor given unauthorized aid on this academic work. 

#%% [markdown]
##### Imports

#%%
# region imports ----------------------------------------
# import python packages
import pandas as pd
#%matplotlib inline
import matplotlib.pyplot as plt
import re
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import os

import numpy as np
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk import FreqDist, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob

# Vader sentiment
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

from pattern.en import sentiment

# endregion 

#%% [markdown]
# region Business Understanding
## Business Understanding

# The purpose of this project is to try and predict if a particular TV show will be either renewed or canceled. 
# This will be based on data collected and analyzed from IMDb and twitter. In particular, I will try to gauge the
# shows popularity by:
# * looking at the IMDb score and the number of users who voted
# * analyzing sentiment of the reviews 
# * analyzing review scores
# * analyzing the shows popularity by it twitter following
#
#
# If sucessful, the real world applications of this could be: 
# * Help networks decide whether or not to renew or cancel a show
# * Could help entertainment news agencies better predict a show's renewal\cancelation
#
#
# The question I would like to answer are:
# 1. Does a strong twitter following lead to a shows renewnal?
# 2. Can the shows IMDb score help to predict it's cancelation?
# 3. Is there a coorelation to the sentiment from the shows reviews and it being renewed\canceled?
#
# endregion

#%% [markdown]
# region sources
### Sources:
# The source of the data comes from 3 places, Metacritc, IMDb and Twitter. 
# 
#
# The data collected from metacritic includes: 
# * TV show name
# * Renewed\Cancel status
# * Network show aired on
# 
#
# The data collected from IMDb includes: 
# * Title
# * IMDb Score
# * Number of users voted
# * If applicable, the shows ranking within IMDb top 250 TV shows
# * Keywords
# * Genres
# * Content rating
# * Country
# * Language
# * Release Date
# * Runtime
# * TV Network 
# 
#
# The Data Collected from Twitter includes: 
# * Name
# * twitter handle (screenname)
# * number of followers
# endregion

#%% [markdown]

# region data collection tech
### Data Collection Techniques
# The methods for collecting the data was web crawling and the Twitter API
# 
# The code for data collection was written in python seperate from the Juptyer Notebook and can be
# found in the GIT repository. See below for a detailed explaination:
# 
# The data collection was split into three parts: 
# 1. Getting the appropiate IMDb links
# 2. Getting the appropiate IMDb Data
# 3. Getting the appropiate Twitter data
#
#
# The first step was to scrape the metacritic website to get a list of renewed\canceled TV shows. 
# Once completed, I could use the shows name to build an IMDb query url in order to find all the IMDb Links 
# associated with the show name. There were some issues were the search string wasn't quite right and IMDb 
# resulted in incorrect results. These were very few and were not added to the final list.
# he code for the link collection can be found in the Get_IMDb_Links folder.
#
# The second step was to collect the IMDb data for each of the links created from the first step. 
# All the data was collected using Beatiful Soup instead of xpath extraction. The code can be found in the 
# Get_IMDb_Data folder.
#
# The last step was to collect the Twitter data. This step turned out to be the most challanging as most of
# of the shows didn't have an Official Site embeded in its IMDb page. I used the Python paclage Tweepy to 
# search twitter for users with the query string being the show name. In some cases, I added the network to the
# query string.
#
# In the case where I did have a link from IMDb to the shows Official Twitter page, I noticed that some of those links
# were not working. I found out that was due the fact that the tokens have updated thus invalidating the originally collected
# link from IMDb. Instead of using the links I had already collected, I decided to collect the link at the time of needing
# it. From there I used Beatiful Soup to scrape the twitter handle and later pushed it through the twitter API 
# to get the information needed.
#
# Since twitter's search users api call returns multiple results, I created a crude algorithm in order to 
# determine the most likely twitter account. For example, the show Zoo shows results from different city 
# zoos. I needed to determine which twitter user was more likely to be the TV show. I did this by implementing
# a series of checks that look at the Twitter users name, screenname, and description and I check it against
# the characteristic of the show (network, name, etc). In addition, if the account is verified, I increase the 
# measured weight. This proved to be very accurate with only a few being incorrect, these are still in the 
# dataset. 
#
# The code for the Twitter data collection can be found in the Get_social_media_data folder.

# endregion

#%% [markdown]

## Data cleaning & Text Pre-Processing

#%%
# This function is to read the json files

def read_json(filename):
    path = os.path.join('Predict_TV_Show_Cancelation', 'Data', filename)

    with open(path, 'r') as infile: 
        return infile

#%%
# Data is spilt into three json files: 1. IMDb Data, 2. IMDb Reviews, 3. Twitter Data

# Get the data
rescuedIMDbData = read_json('rescued_IMDB_Data.json')
rescuedIMDbReviews = read_json('rescued_imdb_reviews.json')
rescuedTwiterData = read_json('rescuedTwitterData.json')

print(rescuedIMDbData)