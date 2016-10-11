# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 15:12:14 2016

@author: msrareg3
"""

import networkx as nx
import numpy as np
import pandas as pd

# import weighted adj matrices, convert into graphs
df = pd.read_csv('modxmod.csv', index_col=0)
df2 = pd.read_csv('subxsub.csv', index_col=0)

# 
m = np.nan_to_num(np.matrix(df))
np.fill_diagonal(m,0) # trying to correct for isolates, why nec?
M=nx.from_numpy_matrix(m)

s = np.nan_to_num(np.matrix(df2))
np.fill_diagonal(s,0)
S=nx.from_numpy_matrix(s)


# create mapping dict to relabel nodes
def get_index_names_dict(df):
    '''takes df where index is list of names
       returns dict of index number:name'''
    d = {}
    for i in range(len(df.index)):
        d[i] = df.index[i]
    return d

M_names = get_index_names_dict(df)
nx.relabel_nodes(M,M_names,copy=False)

S_names = get_index_names_dict(df2)
nx.relabel_nodes(S,S_names,copy=False)

# checking isolates
for x in nx.isolates(M):
    print x, df[x].sum()

for x in nx.isolates(S):
    print x, df2[x].sum()
    
# removing isolates from graph
M.remove_nodes_from(nx.isolates(M))
nx.draw(M,with_labels=True)

S.remove_nodes_from(nx.isolates(S))
nx.draw(S, with_labels=True)


# get all moderators, not just originals
df = pd.read_csv('default_subs_mods.csv')
df['value'] = 1
sub_mod_matrix = df.pivot('subreddit', 'name','value')
a = np.matrix(sub_mod_matrix)
a = np.nan_to_num(a)
a = np.dot(a,np.transpose(a))
np.fill_diagonal(a,0)
G=nx.from_numpy_matrix(a)
G_names = get_index_names_dict(sub_mod_matrix)
nx.relabel_nodes(G,G_names,copy=False)
nx.draw(G, with_labels=True)

df = pd.read_csv('default_subs_mods.csv')
df['value'] = 1
mod_sub_matrix = df.pivot('name','subreddit', 'value')
a = np.matrix(mod_sub_matrix)
a = np.nan_to_num(a)
a = np.dot(a,np.transpose(a))
np.fill_diagonal(a,0)
G2=nx.from_numpy_matrix(a)
G2_names = get_index_names_dict(mod_sub_matrix)
nx.relabel_nodes(G2,G2_names,copy=False)

nx.draw(G2, with_labels=True)


