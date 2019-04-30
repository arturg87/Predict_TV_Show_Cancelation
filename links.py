from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import re
import json
import os

url_base = 'https://www.imdb.com%s'

class get_links:
    def __init__(self):
        self.imdb_link_data = []
        
    def get_IMDb_links(self, show_name):
        # Store IMDb Link Data
        stoplist = ['Marvel\'s']
        
        for word in show_name.split():
            if word == 'SVU':
                show_name = re.sub('SVU', 'Special Victims Unit', show_name)
            if word in stoplist:
                show_name = re.sub(word+" ", '', show_name)
                
        # serialize the tv show name to handle special characters and whitspace.
        show_name_serial = quote(show_name)
        show_name_serial = show_name_serial.lower()

        # build the IMDb query url.
        url = 'https://www.imdb.com/search/title?title=%s&title_type=tv_series&view=simple' %(show_name_serial)
        
        http = urllib3.PoolManager()
        fp = http.request('GET', url)
        soup = BeautifulSoup(fp.data, features='lxml')

        data = soup.find_all('div', {'class':'article'})

        for i in data: 
            if "No results" in i.find('div', {'class':'desc'}).text.strip():
                link = "Show Not Found"
                title = show_name
                break
            else:
                for n in i.find_all('div', {'class':'col-title'}):
                    title = n.find('a').text.strip()
                    link = url_base %(n.find('a').get('href'))

                    if internal_check_name(show_name, title):
                        break
                    else:
                        title = show_name
                        link  = "Show Not Found"

                    #sectionText = n.find('h3', {'class':'findSectionHeader'}).text
                    #if "Titles" in sectionText:
                    #    link, title = internal_linking(n, show_name)                       

            if link == "Show Not Found":
                pass
            else:
                self.imdb_link_data.append({
                    'tv_show_imdb_link':link,
                    'tv_show_name':[title]
                })

        print(show_name, title, link)
        time.sleep(0.3)

    def write_json(self, which_type):
        if which_type == "renewed":
            filename = 'renewed.json'
        elif which_type == "canceled":
            filename = 'canceled.json'
        elif which_type == "rescued":
            filename = 'rescued.json'

        path = 'Predict_TV_Show_Cancelation//Data'
        with open(os.path.join(path, filename), 'w') as outfile:
            json.dump(self.imdb_link_data, outfile)


def internal_check_name(show_name, titleToCheck):
    flag = False

    test_list = ['Rapunzel\'s Tangled Adventure', '100 000 Pyramid', 'Anne With an E', 'The Circus', 'Floribama Shore', 'Me Myself   I']
    show_name = re.sub('[^a-zA-Z0-9]', ' ', show_name).strip()
    titleToCheck = re.sub('[^a-zA-Z0-9]', ' ', titleToCheck).strip()

    if show_name.lower() == titleToCheck.lower():
        return True

    if show_name in test_list:
        for word in show_name.split():
            if str(word).lower() in str(titleToCheck).lower() and str(word).lower() != "the":
                flag = True
                return flag
            else:
                flag = False

    return flag
    