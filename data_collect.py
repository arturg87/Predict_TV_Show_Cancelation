#%% [markdown]
#### Import Packages

#%%

# import python packages
import requests
from lxml import html
import csv
import pandas as pd
#%matplotlib inline
import matplotlib.pyplot as plt

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

import numpy as np
from collections import Counter

# import nltk (natural language tool kit), a popular python package for text mining
import nltk
# stopwords, FreqDist, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WorpytpipdNetLemmatizer

from nltk.corpus import stopwords
from textblob import TextBlob

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

from pattern.en import sentiment

from os import path

# Import and Function too allow using markdown print in Code
from IPython.display import Markdown, display

def printmd(str):
    display(Markdown(str))

import re

#%% [markdown]
# Business Understanding

#%% [markodwn]
