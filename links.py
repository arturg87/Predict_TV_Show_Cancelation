from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

import json

class get_links:
    def __init__(self):
        self.imdb_link_data = []

    def get_IMDb_links(self, show_name):
        # Store IMDb Link Data

        # serialize the tv show name to handle special characters and whitspace.
        show_name_serial = quote(show_name)

        # build the IMDb query url.
        url = 'https://www.imdb.com/find?ref_=nv_sr_fn&q=%s' %(show_name_serial)
        url_base = 'https://www.imdb.com%s'
        http = urllib3.PoolManager()
        fp = http.request('GET', url)
        soup = BeautifulSoup(fp.data, features='lxml')

        data = soup.find_all('div', {'class':'article'})

        for i in data: 
            if "No Results" in i.find('h1', {'class':'findHeader'}).text.strip():
                link = "n/a"
                title = show_name
                break
            else:
                for n in i.find_all('div', {'class':'findSection'}):
                    if "Titles" in n.find('h3', {'class':'findSectionHeader'}).text and "TV Series" in n.find('td', {'class':'result_text'}).text:
                        link = url_base %(n.find('td', {'class':'result_text'}).find('a').get('href'))
                        title = n.find_all('td', {'class':'result_text'})[0].find('a').text
                        break
                    else:
                        link = "n/a"
                        title = show_name

                flag = False
                for word in show_name.split():
                    if str(word).lower() in str(title).lower() and str(word).lower() != "the":
                        flag = True
                        break
                    else:
                        flag = False

                if flag == False:
                    link = "n/a"
                    title = show_name                  
                
            self.imdb_link_data.append({
                'tv_show_imdb_link':link,
                'tv_show_name':[title]
            })
        print(show_name, title, link)
        time.sleep(0.3)

    def write_json(self, which_type):
        if which_type == "renewed":
            filename = 'renewed.json'
        elif "canceled":
            filename = 'canceled.json'
        elif "rescued":
            filename = 'rescued.json'
        with open(filename, 'w') as outfile:
            json.dump(self.imdb_link_data, outfile)