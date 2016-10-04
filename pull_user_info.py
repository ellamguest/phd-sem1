# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 15:45:20 2016

@author: msrareg3
"""

import requests
import json

def get_user_trophies(user):
    trophies = requests.get('https://www.reddit.com/user/{}/trophies/.json'.format(user), headers=headers)
    trophies_data = trophies.json()
    x = list()
    for i in range(len(trophies_data['data']['trophies'])):
        x.append(trophies_data['data']['trophies'][i]['data']['name'])
    return x

get_user_trophies('qgyh2')