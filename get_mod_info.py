# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:51:58 2016

@author: msrareg3
"""
import requests
import pandas as pd
from datetime import datetime

headers={'User-agent':'wednesdaysguest bot 0.1'}

df = pd.read_csv('default_abouts.csv', index_col=0)
subs = df['display_name']

# GETTING MODERATION DATA

def pull_sub_data(subreddit):
    '''subreddit ex. 'gadgets', datatype ex. 'about/moderators' '''
    BASE_URL = 'https://www.reddit.com/r/'
    query = '/about/moderators.json'
    url = BASE_URL + subreddit + query
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['data']['children']

dfs = []
for i in range(len(subs)):
    data = pull_sub_data(subs[i])
    d = pd.DataFrame.from_dict(data)
    d['subreddit'] = subs[i]
    dfs.append(d)
mdf = pd.concat(dfs)
mdf.index.names = ['order']
mdf.reset_index(inplace=True)
mdf['time'] = pd.to_datetime(mdf.date, unit='s', format='%Y/%m/%d')


mdf.to_csv('def_mods.csv')
mdf = pd.read_csv('def_mods.csv', index_col=0)

# LOOK AT REPEAT MODERATORS

def get_repeat_names(df):
    x = df.groupby('name')['name'].count()
    x.sort(ascending=False)
    return x[x>1]

names = list(get_repeat_names(mdf).index)
repeats = mdf.loc[mdf['name'].isin(names)]
repeats['value']=1

am = repeats.pivot('name','subreddit','value').fillna(0)

