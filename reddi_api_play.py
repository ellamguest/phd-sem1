# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 13:59:18 2016

@author: emg
"""
# HOW TO LOG INTO ACCOUNT FOR FULL ACCESS?
from pprint import pprint
import requests
import json
import ijson
import pandas as pd

headers={'User-agent':'wednesdaysguest bot 0.1'}

####### USER INFO

username = 'bluecoffee'
# 'wednesdaysguest'

r = requests.get('https://www.reddit.com/user/{}/comments/.json'.format(username), 
                 headers=headers)
data = r.json()
print data.keys()


trophies = requests.get('https://www.reddit.com/user/{}/trophies/.json'.format(username),
                        headers=headers)
trophies_data = trophies.json()
print trophies_data

about = requests.get('https://www.reddit.com/user/{}/about/.json'.format(username),
                     headers=headers)
about_data = about.json()
about_data
'''' about = created, has_verified_email, hide_from_robots, id, is_friend,
 is_gold, is_mod, link_karma, name, kind ''''

def pull_user_data(user, datatype):
    '''user ex. 'username', datatype ex. 'comments' '''
    r = requests.get('https://www.reddit.com/user/{}/{}.json'.format(user, datatype),
                     headers=headers)
    return r.json()
    
pull_user_data(username, 'about')

####### SUBREDDIT INFO

default_subs = requests.get('https://www.reddit.com/subreddits/default.json', headers={'User-agent': 'wednesdaysguest bot 0.1'}).json()

####### DUMPING INFO

# trying to convert json to pandas
#objects = ijson.items(default_subs, '...'

# save json data to text file
with open('default_subs.txt', 'w') as outfile:
    json.dump(default_subs, outfile)
    
# open json data from text file
with open('default_subs.txt') as json_data:
    d = json.load(json_data)

'''# d.keys() = kind, data
# d['kind'] = 'Listing
d['data'] = dict of everything else
'''
d_data = d['data']
''' d_data.keys()
[u'modhash', u'children', u'after', u'before']
modhash = empty
children = everything, a list? of 25 objects (so only brought me first 25?)
after = t5_2qnts (how ot I find subreddit by id?)
before = empty
'''
data = d['data']['children']
''' list of 25 dicts
keys = [u'kind', u'data']
data[0]['data'].keys() = 44
'''

# CREATE DATAFRAME
df = pd.DataFrame(columns=data[0]['data'].keys())
for i in range(len(data)):
    df = df.append(data[i]['data'], ignore_index=True)

# name display_name first column
cols = df.columns.tolist()
cols = [cols[8]] + cols[:8] + cols[9:]
df=df[cols]