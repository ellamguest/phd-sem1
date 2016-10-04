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


def get_repeat_names(df):
    x = df.groupby('name')['name'].count()
    x.sort(ascending=False)
    return x[x>1]
    
# GET REPEAT DEFAULT MODS
x = default_subs_mods.groupby('name')['name'].count()
x.sort(ascending=False)
repeat_default_mods= x[x>1]

# GET DEFAULT CREATORS (OR OLDEST MODERATORS AT LEAST)
first_mods = df[df.index == 0]
repeat_first_mods = get_repeat_names(first_mods)

# ATTEMPTING TO GET ALL DEFAULT MODS

                   