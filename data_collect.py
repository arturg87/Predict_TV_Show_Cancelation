import requests
from lxml import html
import csv

import links
import functions

from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from os import path

## Get list of canceled/renewed TV shows
http = urllib3.PoolManager()

url = 'https://www.metacritic.com/feature/tv-renewal-scorecard-2017-2018-season'

fp = http.request('GET', url)
soup = BeautifulSoup(fp.data, features='lxml')
data = soup.find_all('p', {'class':'medium'})

func = functions.get_data()
links = links.get_links()

for text in data: 
    if "has renewed" in text.text or "renewed for" in text.text:
        func.is_renewed(text)
    elif "canceled" in text.text:
        func.is_canceled(text)
    if "rescued" in text.text:
        func.is_rescued(text)

for i in func.removeFromCanceled:
    func.canceled = [x for x in func.canceled if x != i]

func.remove_duplicates()

for show in func.rescued:
    links.get_IMDb_links(show)
    
links.write_json('rescued')

for show in func.canceled:
    links.get_IMDb_links(show)

links.write_json('canceled')  
  
for show in func.renewed:
    links.get_IMDb_links(show)

links.write_json('renewed')


print(func.renewed)
print()
print(func.canceled)
print()
print(func.rescued)

print()