from datetime import time
from datetime import datetime
from time import strptime
import dateutil.parser as dp
from isodate import parse_duration

imdbData = [{'tv_show_name': 'Brooklyn Nine-Nine', 'imdb_score': 8.4, 'imdb_score_num_users': 144529, 'top_rated_rank': '238', 'story_keywords': ['police', 'new york city', 'police detective', 'police captain', 'female cop'], 'genres': ['Comedy', 'Crime'], 'tv_rating': 'TV-14', 'country': ['USA'], 'langauge': ['English'], 'release_date': '17 September 2013', 'runtime': 'PT22M', 'tv_network': None, 'twitter_followers': None, 'twitter_screenname': None}]
reviewData = [{'tv_show_name': 'Brooklyn Nine-Nine', 'pos_review_sent': 56, 'neg_review_sent': 9, 'neut_review_sent': 10, 'pos_revTitle_sent': 56, 'neg_revTitle_sent': 9, 'neut_revTitle_sent': 10}]
twitterData = [{'tv_show_name': 'Brooklyn Nine-Nine', 'twitter_data': {'name': 'Brooklyn Nine-Nine', 'screen_name': 'nbcbrooklyn99', 'followers_count': 607086}}]

def merge_lists(l1, l2, key, typeSM):
    merged = {}
    count = 0
    for item in l1+l2:
        if item[key] in merged:
            if typeSM == 'twitter':
                try:
                    twitter = {"twitter_followers":l2[count]['twitter_data']['followers_count'], 'twitter_screenname':l2[count]['twitter_data']['screen_name']}
                    merged[item[key]].update(twitter)
                except:
                    twitter = {"twitter_followers": None, 'twitter_screenname': None}
                    merged[item[key]].update(twitter)
            elif typeSM == 'review':
                if item[key] in merged:
                    merged[item[key]].update(item)
            count += 1
        else:
            merged[item[key]] = item
    
    for (_, val) in merged.items():
        items = val
        try:
            if items['twitter_followers'] or not items['twitter_followers']:
                pass
        except:
            twitter = {"twitter_followers": None, 'twitter_screenname': None}
            #for each in followers:
            merged[items['tv_show_name']].update(twitter)

    return [val for (_, val) in merged.items()]


runtime = 'PT30M'
fmt = '%M'
p = parse_duration(runtime)

p.totimedelta
print(time.strftime(p, '%M'))


print(merge_lists(imdbData,twitterData, 'tv_show_name', 'twitter'))
print(merge_lists(imdbData,reviewData, 'tv_show_name', 'review'))