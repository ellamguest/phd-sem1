# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:38:43 2016

@author: emg
"""
import pandas as pd
import numpy as np 

#df = pd.read_csv('/Users/emg/Programmming/GitHub/phd-sem1/mod_by_sub_matrix.csv')
#df = df.drop('name', axis=1)
#a = df.as_matrix()
#m = np.matrix(a)
#
#mat = np.dot(m.transpose(), m)


df = pd.read_csv('default_subs_mods.csv')
df['value'] = 1
aff = df.pivot('subreddit', 'name','value').fillna(0)
a = aff.as_matrix()
m = np.matrix(a)
mat = np.dot(m, m.transpose())

d = pd.DataFrame(mat)
d.to_csv('/Users/emg/Programmming/GitHub/R-phd-sem-1/full_weighted_net.csv',index=False)

# GETTING SUBREDDIT ATTRIBUTES LIST

df = pd.read_csv('/Users/emg/Programmming/GitHub/phd-sem1/default_subs.csv')
att = df[['display_name','subscribers']]
att.sort_values('display_name', inplace=True)
att.reset_index(drop=True, inplace=True)
att.rename(columns={'display_name':'subreddit'}, inplace=True)
att.to_csv('/Users/emg/Programmming/GitHub/R-phd-sem-1/default_attributes.csv', index=True)