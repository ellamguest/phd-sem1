# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:48:16 2016

@author: emg
"""

import pandas as pd

# RELABELLING AFFILIATION MATRIX IDS
df = pd.read_csv('/Users/emg/Programmming/R/polnet2016/Data files/reddit/def_mod_aff.csv', index_col='name')

def relabel(dimension, letter):
#    dimension = df.columns or df.index 
#   letter = s or m
    labels = []
    for i in range(len(dimension)):
        labels.append("{0}{1:0=2d}".format(letter,i+1))
    return labels

df.columns = relabel(df.columns, 's')
df.index = relabel(df.index, 'm')

df.to_csv('/Users/emg/Programmming/R/polnet2016/Data files/reddit/def_mod_aff_ids.csv')


# CREATING EDGELIST
# import df of moderator attributes
df = pd.read_csv('/Users/emg/Programmming/GitHub/phd-sem1/default_subs_mods.csv')
df = df[df['Unnamed: 0'] == 0]
df = df[['name','subreddit']]
df['weight'] = 1

df.to_csv('/Users/emg/Programmming/R/polnet2016/Data files/reddit/def_mod_edgelist.csv')

ids = df
ids['subreddit'] = relabel(ids['subreddit'], 's')
ids['name'] = relabel(ids['name'], 'm')
ids = ids.reset_index(drop=True)

ids.to_csv('/Users/emg/Programmming/R/polnet2016/Data files/reddit/def_mod_edgelist_ids.csv'