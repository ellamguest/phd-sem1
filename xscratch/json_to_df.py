# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 13:43:59 2016

@author: msrareg3
"""
import requests
import json
import pandas as pd

headers={'User-agent':'wednesdaysguest bot 0.1'}
username = 'wednesdaysguest'

# REQUEST LISTINGS OF DEFAULT SUBS

default_subs1 = requests.get('https://www.reddit.com/subreddits/default.json',
                            headers=headers).json()                        
default_subs2 = requests.get('https://www.reddit.com/subreddits/default/.json?after=t5_2qnts',
                             headers=headers).json()
default_subs = default_subs1['data']['children'] + default_subs2['data']['children']

# CREATE DATAFRAME OF LISTING INFO FROM JSON OBJECT
def json_to_df(json_info):
    # json_info should be in the form d['data']['children']
    # convert json object info to pandas dataframe
    df = pd.DataFrame(columns=json_info[0]['data'].keys())
    for i in range(len(json_info)):
        df = df.append(json_info[i]['data'], ignore_index=True)
    return df

df = json_to_df(default_subs)
# MAKE NAME FIRST CLOUMN FOR DEFAULT SUB INFO
cols = df.columns.tolist()
#cols = [cols[8]] + cols[:8] + cols[9:]
df = df[[cols[8]] + cols[:8] + cols[9:]]

df.to_csv('default_subs.csv', header=True, index=True, encoding='utf-8')

print df.head()