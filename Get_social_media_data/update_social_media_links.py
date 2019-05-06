from bs4 import BeautifulSoup
import urllib3
import re 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class updateSMLink():

    def updateLinks(self, tvShowLink, officialType):
        soup = load_url(tvShowLink)

        try:
            details = soup.find('div', {'id':'titleDetails'})

            imdbLink = tvShowLink
            movieID = re.search("(tt[0-9]{7})", imdbLink).group()
            baseExtUrl = "https://www.imdb.com/title/%s/" %(movieID)
            baseUrl = "https://www.imdb.com"

            for each in details.contents:
                try:
                    # If IMDb page has Official Sites in the Details section, pull each site and store in list
                    if "official sites" in each.text.lower():
                        sites = []
                        for lnk in each.findAll('a'):
                            # If there is a see more link within the Official Sites section, pull the URL so we can pull data from that url
                            if "see more" in lnk.text.lower():                    
                                sitesListUrl = baseExtUrl + lnk.get('href')
                            else: 
                                sitesListUrl = None

                        # If there is no "see more" link, pull whatever official site link data there is.
                        if sitesListUrl == None: 
                            for lnk in each.findAll('a'):
                                if "official" in lnk.text.lower() and "site" not in lnk.text.lower():
                                    sites.append({
                                        'social_media_site': lnk.text,
                                        'social_media_link': baseUrl + lnk.get('href')
                                    })
                        else:
                            #baseUrl = "https://www.imdb.com"
                            
                            # since there is additional link than what is displayed, we will pull data from that list.
                            linkDataSoup = load_url(sitesListUrl)

                            officalLinks = linkDataSoup.find('ul', {'class':'simpleList'}).findAll('a')

                            for lnk in officalLinks:
                                if "official" in lnk.text.lower() and "site" not in lnk.text.lower():
                                    sites.append({
                                        'social_media_site': lnk.text,
                                        'social_media_link': baseUrl + lnk.get('href')
                                    })
                        break
                except:
                    sites = None
                    pass
        except:
            sites = None
        
        # if the data we pulled matches the social media site we request, return the URL found in IMDb
        for i in sites:
            if i['social_media_site'] == officialType:
                return i['social_media_link']


def load_url(url):
    # Load the passed in url and get the html data for it
    try:

        http = urllib3.PoolManager()
        fp = http.request('GET', url)
        soup = BeautifulSoup(fp.data, features='lxml')
    except:
        print("url not found")
    return soup