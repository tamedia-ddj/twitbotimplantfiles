# coding: utf-8

from twython import Twython
import pandas as pd
import time
from datetime import datetime
import dateutil.parser
import numpy as np
import json
import progressbar
import sys

# ### Documentation
# [Searching Twitter](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets)
# [Twython Documentation](https://twython.readthedocs.io/en/latest/api.html)

#CREDENTIALS_FILENAME = 'creds_twitter2.json'
CREDENTIALS_FILENAME = 'twitimplantfiles/creds_twitter2.json'
jf = open(CREDENTIALS_FILENAME)
creds = json.load(jf)
jf.close()

twitter = Twython(creds['consumer_key'], creds['consumer_secret'],
                 creds['access_token'], creds['access_token_secret'])

#Put it all together, so I can do as much as I like
bar = progressbar.ProgressBar()
lst = []
if twitter.search(q='implantfiles', count=1)['statuses'] == []:
    sys.exit()
else:
    max_id = twitter.search(q='implantfiles', count=1)['statuses'][0]['id_str']
    count = 0

    #Getting Followers of indiviual users
    for elem, i in zip(range(50), bar(range(50))):
        result = twitter.search(q='implantfiles',
                                count=100,
                                max_id=max_id,
                                tweet_mode='extended')
    #Updating list with name of head account
        for elem in result['statuses']:

                full_text = elem['full_text'].replace("\n", " ")
                id_str = elem['id_str']
                user = elem['user']['screen_name']
                place = elem['place']
                geo = elem['geo']
                descr = elem['user']['description']
                created_at = elem['created_at']

                mini_dict = {'Full Text':full_text,
                         'ID':id_str,
                         'User': user,
                         'Place': place,
                         'Geo': geo,
                         'Descr': descr,
                         'Date': created_at}

                lst.append(mini_dict)

                max_id = elem['id_str']

    #Saving
    df = pd.DataFrame(lst)
    df.to_csv('twitimplantfiles/d/'+str(datetime.now())+".csv")
    #df.to_csv('d/'+str(datetime.now())+".csv")
