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

def get_user_trophies(user):
trophies = requests.get('https://www.reddit.com/user/{}/trophies/.json'.format('qgyh2'),
                        headers=headers)
trophies_data = trophies.json()
print trophies_data

x = list()
for i in range(len(trophies_data['data']['trophies'])):
    x.append(trophies_data['data']['trophies'][i]['data']['name'])

get_user_trophies

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



