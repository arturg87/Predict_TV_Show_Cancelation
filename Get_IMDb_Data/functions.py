from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import json
import os
from os import path
import re 

class load_func:

    def __init__(self):
        self.tv_show_data = []

    def load_json(self, name):
        base_json_path = "Predict_TV_Show_Cancelation"

        with open(path.join(base_json_path, "Data", name), 'r') as f:
            tv_shows = json.load(f)

        return tv_shows

    # ---------------------------------------------------------------------------------------------------

    def get_imdb_data(self, json_data):
        soup = load_url(json_data['tv_show_imdb_link'])
        #soup = BeautifulSoup(open('Predict_TV_Show_Cancelation\\Data\\b99.html'), "html.parser")
        
        # region Get Tite -------------------------------------------
        try:
            # Get Title
            title = soup.find('div', {'class':'title_wrapper'}).find('h1').text.strip()
        except Exception as e:
            #print("Could not get title for %s" %(json_data['tv_show_name']))
            title = None

        # endregion -------------------------------------------------

        # region Get IMDB Score -------------------------------------
        try:
            #Get IMDB score and number of users based on
            ratingText = soup.find('div', {'class':'ratingValue'}).find('strong')['title']
            ratingText = re.sub(',', '', ratingText)
            imdbScore = float(re.search(r'(\d.\d*) based on (\d*)', ratingText).group(1))
            imdbScoreNumUsers = int(re.search(r'(\d.\d*) based on (\d*)', ratingText).group(2))

        except Exception as e:
            #print("Could not get IMDb Score for %s" %(json_data['tv_show_name']))
            imdbScore = None
            imdbScoreNumUsers = None

        # endregion --------------------------------------------------------

        # region Get Awards -----------------------------------------
        try:
            # Get Awards
            awardSection = soup.find('div', {'id':'titleAwardsRanks'})

            for each in awardSection.contents:
                try:
                    if "top rated" in each.text.strip().lower():
                        topRatedRank = re.search(r'(\d{1,})', each.text.strip()).group(1)
                        break
                except:
                    topRatedRank = None
                    pass
                
                #try:
                #    if "golden globe" in each.text.lower():
                #        goldenGlobeWon = re.search(r'(\d{1,})', each.text.strip()).group(1)
                #except:
                #    print("%s does not have any golden globes" %(title))
                #    pass
                
        except Exception as e:
            topRatedRank = None

        # endregion --------------------------------------------------------

        # region Storyline ------------------------------------------
        try:
            storyline = soup.find('div', {'id':'titleStoryLine'})
        
        except Exception as e:
            storyline = None
        
        # endregion -------------------------------------------------

        # region Plot Keywords -------------------------------------
        try:
            for each in storyline.contents:
                try:
                    keywords = []

                    if "plot keywords" in each.text.lower().strip():
                        for text in each.findAll('a'):
                            if "see all" not in text.text.lower():
                                keywords.append(text.text.strip())  
                        break
                except Exception as e:
                    keywords = None
                    pass

        except Exception as e:
            keywords = None
        # endregion -------------------------------------------------

        # region Genres ----------------------------------------------
        try:
            
            for each in storyline.contents:
                try:
                    genres = []

                    if "genres" in each.text.lower().strip():
                        for text in each.findAll('a'):
                            if "see all" not in text.text.lower():
                                genres.append(text.text.strip())
                    
                        break
                except:
                    genres = None
                    pass
                
        except Exception as e:
            genres = None
        # endregion -------------------------------------------------

        # region TV Rating-------------------------------------------
        try:
            for each in storyline.contents:
                try:
                    if "certificate" in each.text.lower().strip():
                        tvRating = each.find('span').text
                        break
                except:
                    tvRating = None
                    pass

        except Exception as e:
            tvRating = None
        # endregion -------------------------------------------------

        # region Details section ------------------------------------
        try:
            details = soup.find('div', {'id':'titleDetails'})

        except Exception as e:
            details = None
        # endregion -------------------------------------------------

        # region Official Sites  ------------------------------------
        try:
            

            imdbLink = json_data['tv_show_imdb_link']
            movieID = re.search("(tt[0-9]{7})", imdbLink).group()
            baseUrl = "https://www.imdb.com/title/%s/" %(movieID)

            for each in details.contents:
                try:
                    if "official sites" in each.text.lower():
                        sites = []
                        for lnk in each.findAll('a'):
                            if "see more" in lnk.text.lower():                    
                                sitesListUrl = baseUrl + lnk.get('href')
                            else: 
                                sitesListUrl = None

                        if sitesListUrl == None: 
                            for lnk in each.findAll('a'):
                                if "official" in lnk.text.lower() and "site" not in lnk.text.lower():
                                    sites.append({
                                        'social_media_site': lnk.text,
                                        'social_media_link': baseUrl + lnk.get('href')
                                    })
                        else:
                            baseUrl = "https://www.imdb.com"

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
        except Exception as e:
            sites = None
        # endregion -------------------------------------------------

        # region Country section ------------------------------------
        try:
            
            for each in details.contents:
                try:
                    country = []
                    if "country" in each.text.lower():
                        for lnk in each.findAll('a'):
                            country.append(lnk.text.strip())
                        break
                except:
                    country = None
                    pass

        except Exception as e:
            country = None
        # endregion -------------------------------------------------

        # region Language section -----------------------------------
        try:
            
            for each in details.contents:
                try:
                    language = []

                    if "language" in each.text.lower():
                        for lnk in each.findAll('a'):
                            language.append(lnk.text.strip())
                        break
                except:
                    language = None
                    pass

        except Exception as e:
            language = None
        # endregion -------------------------------------------------

        # region release Date section -------------------------------
        try:
            for each in details.contents:
                try:
                    if "release date" in each.text.lower():
                        releaseDate = each.text.strip()
                        releaseDate = re.search(r'\d(.*)\d{4}', releaseDate).group()
                        break
                except:
                    releaseDate = None
                    pass

        except Exception as e:
            releaseDate = None
        # endregion -------------------------------------------------

        # region runtime Date section -------------------------------
        try:
            for each in details.contents:
                try:
                    if "runtime" in each.text.lower():
                        runtime = each.find('time')['datetime'] 
                        break
                except:
                    runtime = None
                    pass

        except Exception as e:
            runtime = None
        # endregion -------------------------------------------------

        # region user reviews section --------------------------------
        reviews = []

        imdbLink = json_data['tv_show_imdb_link']
        movieID = re.search(r"(tt[0-9]{7})", imdbLink).group()
        baseUrl = "https://www.imdb.com/title/%s/reviews/_ajax" %(movieID)
        paginationUrl = "?ref_=undefined&paginationKey="    
    
        reviewsSoup = load_url(baseUrl)

        # get next
        for i in range(3):    
            try:
                paginationKey = reviewsSoup.find('div', {'class':'load-more-data'})['data-key']
            except:
                paginationKey = None
                pass

            def beautifulSoupHelper(data, findAllName, findName, findAllAttrs={}, findAttrs={}):
                for stuff in data.findAll(findAllName, findAllAttrs):
                    return stuff.find(findName, findAttrs).text.strip()

            def getReviewData():
                for data in reviewsSoup.findAll('div', {'class':'lister-item'}):
                    try:
                        score = beautifulSoupHelper(data, 'span', 'span', {'class':'rating-other-user-rating'})
                    except:
                        score = None
                        #print("Couldn't get review score for%s " %(title))

                    try:
                        user = beautifulSoupHelper(data, 'span', 'a', {'class':'display-name-link'})
                    except:
                        user = None
                        #print("Couldn't get reviewer's user name for%s" %(title))

                    try:
                        datePosted = data.find('span', {'class':'review-date'}).text.strip()
                    except:
                        datePosted = None
                        #print("Couldn't get review posted date for%s" %(title))

                    try:
                        summaryTitle = data.find('a', {'class':'title'}).text.strip()
                    except:
                        summaryTitle = None
                        #print("Couldn't get review title for%s" %(title))

                    try:
                        reviewText = data.find('div', {'class':'text'}).text.strip()
                    except:
                        reviewText = None
                        #print("Couldn't get review text for%s" %(title))

                    try:
                        percentFoundHelpful = data.find('div', {'class':'actions'}).text.strip()
                        percentFoundHelpful = re.sub(',', '', percentFoundHelpful)
                        precReg = re.search(r'(\d*) out of (\d*)', percentFoundHelpful)
                        percentFoundHelpful = round((int(precReg.group(1)) / int(precReg.group(2)))*100, 2)
                    except:
                        percentFoundHelpful = None
                        #print("Couldn't get helpfullness of review for%s" %(title))

                    reviews.append({
                        'review_score': score, 
                        'review_UID': user, 
                        'review_date': datePosted,
                        'review_title': summaryTitle,
                        'review_text': reviewText,
                        'percent_found_helpful': percentFoundHelpful
                    })
            
            getReviewData()

            if paginationKey is not None:
                newUrl = baseUrl + paginationUrl + paginationKey
                reviewsSoup = load_url(newUrl)
            else:
                pass



        # get list of   
        # endregion --------------------------------------------------

        self.tv_show_data.append({
            'tv_show_name': title, 
            'imdb_score'  : imdbScore,
            'imdb_score_num_users' : imdbScoreNumUsers, 
            'top_rated_rank' :  topRatedRank, 
            'story_keywords' : keywords,
            'genres': genres,
            'tv_rating': tvRating, 
            'official_sites' : sites, 
            'country': country, 
            'langauge': language,
            'release_date': releaseDate,
            'runtime': runtime,
            'user_reviews' : reviews
        })
        print(title)

    def write_json(self, which_type):
            # filenames for specific list type
            if which_type == "renewed":
                filename = 'renewedIMDB_Data.json'
            elif which_type == "canceled":
                filename = 'canceledIMDB_Data.json'
            elif which_type == "rescued":
                filename = 'rescuedIMDB_Data.json'

            path = 'Predict_TV_Show_Cancelation//Data'

            with open(os.path.join(path, filename), 'w') as outfile:
                outfile.write('[')
                outfile.write('\n')

                count = 1
                for i in self.tv_show_data:
                    json.dump(i, outfile)
                    if count < len(self.tv_show_data):
                        outfile.write(',\n')
                    else:
                        outfile.write('\n')
                    count+=1

                outfile.write(']')   

def load_url(url):
    http = urllib3.PoolManager()
    fp = http.request('GET', url)
    soup = BeautifulSoup(fp.data, features='lxml')
    
    return soup