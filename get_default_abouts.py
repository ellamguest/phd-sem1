# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 10:31:28 2016

@author: msrareg3
"""

import requests
import pandas as pd


# COLLECT DEFAULT SUBREDDIT ABOUT INF0

BASE_URL = 'https://www.reddit.com/'
query = 'subreddits/default.json'
url = BASE_URL + query
headers={'User-agent':'wednesdaysguest bot 0.1'}

response = requests.get(url, headers=headers)
data = response.json()

# SELECT DEFAULT SUBREDDIT NAMES
# subreddit level = data['data']['children'][N]['data']

data['data']['children'][0]['data']['display_name']

names = []
for i in range(len(data['data']['children'])):
    names.append(data['data']['children'][i]['data']['display_name'])

df = pd.DataFrame()
for i in range(len(data['data']['children'])):
    df = df.append(data['data']['children'][i]['data'], ignore_index=True)
    
df.to_csv('default_abouts.csv', encoding= 'utf-8')
df = pd.read_csv('default_abouts.csv', index_col=0)


# PULL MODERATOR INFO FROM SUBREDDIT ABOUT
subs = df['display_name']

def pull_sub_data(subreddit):
    '''subreddit ex. 'gadgets', datatype ex. 'about/moderators' '''
    BASE_URL = 'https://www.reddit.com/r/'
    query = '/about/moderators.json'
    url = BASE_URL + subreddit + query
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['data']['children']

def pull_mod_names(subreddits):
    df = {}
    for i in range(len(subreddits)):
        data = pull_sub_data(subreddits[i])
        names = []
        for n in range(len(data)):
            names.append(data[n]['name'])
        df[subreddits[i]] = names
    return df

df['mods'] = df['display_name'].map(pull_mod_names(subs))


BASE_URL = 'https://www.reddit.com/r/'
query = '/about/moderators.json'
url = BASE_URL + subs[0] + query
r = requests.get(url, headers=headers)
data = r.json()
for i in range len(data['data']['children']):
    info = data['data']['children'][i]

https://www.reddit.com/r/gadgets/about/moderators.json
    
df.to_csv('default_abouts.csv', encoding= 'utf-8')