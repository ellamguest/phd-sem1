# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 10:06:29 2016

@author: emg
"""

import networkx as nx
import numpy as np
import pandas as pd

df = pd.read_csv('default_subs_mods.csv')
df['value'] = 1
df.drop_duplicates('subreddit', inplace=True) # get first moderators

mod_sub_matrix = df.pivot('name', 'subreddit', 'value')
sub_mod_matrix = df.pivot('subreddit', 'name','value')

M_names = mod_sub_matrix.index


# create mapping dict to relabel nodes
def get_index_names_dict(df):
    '''takes df where index is list of names
       returns dict of index number:name'''
    d = {}
    for i in range(len(df.index)):
        d[i] = df.index[i]
    return d
S_names = get_index_names_dict(sub_mod_matrix)
M_names = get_index_names_dict(mod_sub_matrix)


# convert incidence matrices to adjacency
A = np.matrix(mod_sub_matrix)
A = np.nan_to_num(A)
AT = np.matrix(sub_mod_matrix)
AT = np.nan_to_num(AT)
M = np.dot(A,AT) # 2372 x 2372 mods
S = np.dot(AT,A) # 49 x 49 subs

# save and open files
np.savetxt('modxmod.csv',M)
np.savetxt('subxsub.csv',S)
M = np.genfromtxt('modxmod.csv')
S = np.genfromtxt('subxsub.csv')

# convert np matrices to nx graphs and relabel nodes
M=nx.from_numpy_matrix(M)
S=nx.from_numpy_matrix(S)
nx.relabel_nodes(S,S_names,copy=False)
nx.relabel_nodes(M,M_names,copy=False)

# testing networking algorithms
nx.number_connected_components(S)
sorted(nx.degree(S).values())
nx.clustering(S)
nx.degree(S,1)

# drawing network
nx.draw(S)
nx.draw_networkx_labels(S, S_names)