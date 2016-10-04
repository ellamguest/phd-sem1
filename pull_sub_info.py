# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 13:55:24 2016

@author: msrareg3
"""

import requests
import pandas as pd
from json_to_df import df, headers

subs = df['display_name']

def pull_sub_data(subreddit, datatype):
    '''subreddit ex. 'gadgets', datatype ex. 'about/moderators' '''
    r = requests.get('https://www.reddit.com/r/{}/{}.json'.format(subreddit, datatype),
                     headers=headers)
    data = r.json()
    return data['data']['children']

def json_to_df(json_info, subname):
    # json_info should be in the form d['data']['children']
    # convert json object info to pandas dataframe
    df = pd.DataFrame(columns=json_info[0].keys())
    for i in range(len(json_info)):
        df = df.append(json_info[i], ignore_index=True)
        df['subreddit'] = subname
    return df

# GET MODERATOR INFO
def get_sub_mods_df(subs):
    # compile a df of moderators from a list of subreddits
    for i in range(len(subs)):
        if i == 0:
            df = json_to_df(pull_sub_data(subs[0], 'about/moderators'), subs[i])
        else:
            df = df.append(json_to_df(pull_sub_data(subs[i], 'about/moderators'), subs[i]))
    return df
    
default_subs_mods = get_sub_mods_df(subs)
default_subs_mods.to_csv('default_subs_mods.csv')

def get_repeat_names(df):
    x = df.groupby('name')['name'].count()
    x.sort(ascending=False)
    return x[x>1]

default_subs_mods = pd.read_csv('default_subs_mods.csv')

# GET REPEAT DEFAULT MODS
x = default_subs_mods.groupby('name')['name'].count()
x.sort(ascending=False)
repeat_default_mods= x[x>1]
repeat_default_mods.to_csv('repeat_default_mods.csv')
single_default_mods = x[x==1]

# GET DEFAULT CREATORS (OR OLDEST MODERATORS AT LEAST)
first_mods = default_subs_mods[default_subs_mods.index == 0]
repeat_first_mods = get_repeat_names(first_mods)

# GET ENTRIES FOR REPEAT MODS ONLY
names = list(repeat_default_mods.index)
df = default_subs_mods[default_subs_mods['name'].isin(names)] #not sure if this is right!!!!
df = df[['name','subreddit']].sort('name')
df['value'] = 1
df = df.pivot(index='name', columns='subreddit', values='value')
df = df.fillna(value=0)  
df.to_csv('mod_by_sub_matrix.csv')

# TRYING TO CREATE MATRICES TO GRAPH NETWORKS OF CO-MODERATING
mod_sub_matrix = df.as_matrix()             