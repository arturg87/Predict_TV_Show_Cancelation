import links
import functions

from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


## Get list of canceled/renewed TV shows
http = urllib3.PoolManager()

url = 'https://www.metacritic.com/feature/tv-renewal-scorecard-2017-2018-season'

fp = http.request('GET', url)
soup = BeautifulSoup(fp.data, features='lxml')
data = soup.find_all('p', {'class':'medium'})

func = functions.get_data()
links = links.get_links()

#links.get_IMDb_links('$100,000 Pyramid')

# Parse webpage to create a list of canceled\renewed\rescued tv shows
for text in data: 
    if "has renewed" in text.text or "renewed for" in text.text:
        func.is_renewed(text)
    elif "canceled" in text.text:
        func.is_canceled(text)
    if "rescued" in text.text:
        func.is_rescued(text)

# If show was rescued, remove from canceled list if there
for i in func.removeFromCanceled:
    func.canceled = [x for x in func.canceled if not (x['show_name']==i['show_name'])]

# Remove duplcates from all lists
func.remove_duplicates()

# reset link data list
links.imdb_link_data = []

# Get IMDb links\names for all rescued tv shows
for show in func.rescued:
    links.get_IMDb_links(show)
# Write links to JSON file
links.write_json('rescued')


# reset link data list
links.imdb_link_data = []

# Get IMDb links\names for all canceled tv shows
for show in func.canceled:
    links.get_IMDb_links(show)
# Write links to JSON file
links.write_json('canceled')  

# reset link data list
links.imdb_link_data = []

# Get IMDb links\names for all canceled tv shows
for show in func.renewed:
    links.get_IMDb_links(show)
# Write links to JSON file
links.write_json('renewed')