# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:59:28 2016

@author: emg
"""

import pandas as pd 
import re

df = pd.read_csv('/Users/emg/Programmming/GitHub/phd-sem1/default_abouts.csv')


pattern = 'r/([a-z]+)'
df['mentions'] = df['description'].str.findall(pattern)


test = df.loc[48]

df['mentions'][:] = [x for x in df['mentions'] if x != df['display_name']]

def remove_all(element, list):
    return filter(lambda x: x != element, list)

x = remove_all(test['display_name'],test['mentions']) # not working

