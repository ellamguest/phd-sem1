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

username = 'bluecoffee'
# 'wednesdaysguest'

r = requests.get('https://www.reddit.com/user/{}/comments/.json'.format(username), headers={'User-agent': 'wednesdaysguest bot 0.1'}, raw_json=1)
data = r.json()
print data.keys()

print data['data']['children'][0]

for child in data['data']['children']:
    print child['data']['id'],"
    ", child['data']['author'],child['data']['body']
    print

trophies = requests.get('https://www.reddit.com/user/{}/trophies/.json'.format(username), headers={'User-agent': 'wednesdaysguest bot 0.1'})
trophies_data = trophies.json()

about = requests.get('https://www.reddit.com/user/{}/about/.json'.format(username), headers={'User-agent': 'wednesdaysguest bot 0.1'})
about_data = about.json()
about_data
'''' about = created, has_verified_email, hide_from_robots, id, is_friend,
 is_gold, is_mod, link_karma, name, kind ''''

def pull_user_data(user, datatype):
    '''user ex. 'username', datatype ex. 'comments' '''
    r = requests.get('https://www.reddit.com/user/{}/{}.json'.format(user, datatype), headers={'User-agent': 'wednesdaysguest bot 0.1'})
    data = r.json()
    return data
    
pull_user_data('about',username)

default_subs = requests.get('https://www.reddit.com/subreddits/default.json', headers={'User-agent': 'wednesdaysguest bot 0.1'}).json()

# trying to convert json to pandas
#objects = ijson.items(default_subs, '...'

with open('default_subs.txt', 'w') as outfile:
    json.dump(default_subs, outfile)
