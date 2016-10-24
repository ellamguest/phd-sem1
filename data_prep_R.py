# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:48:16 2016

@author: emg
"""

import pandas as pd
import numpy as np

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


# CREATING EDGELIST w/ ids
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

###### ATTETMPING EDGELIST w/out ides

df = pd.read_csv('/Users/emg/Programmming/GitHub/phd-sem1/default_subs_mods.csv')
#orgs = list(df[df['Unnamed: 0'] == 0]['name']) # look at first mods only
#df = df[df['name'].isin(orgs)]
df = df[['name','subreddit', 'date']]
df['weight'] = 1
df = df.reset_index(drop=True)
df.loc[1417,'name'] = 'upliftingnews' #manually change name of user with same name as subreddit

df.to_csv('/Users/emg/Programmming/R/polnet2016/Data files/reddit/edgelist_full.csv', index=False)

# create node attribute list
x = pd.Dataframe()
x['name'] = list(df['name'].unique()) + list(df['subreddit'].unique())
x['type'] = np.where(x['name'].isin(df['name']), 0, 1)

x.to_csv('/Users/emg/Programmming/R/polnet2016/Data files/reddit/nodelist_full.csv', index=False)

      