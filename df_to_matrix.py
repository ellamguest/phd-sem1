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
orgs = df.drop_duplicates('subreddit') # get first moderators
df = df[df['name'].isin(orgs['name'])]

mod_sub_matrix = df.pivot('name', 'subreddit', 'value')
sub_mod_matrix = df.pivot('subreddit', 'name','value')


# save and open files
df = pd.DataFrame(M, index=mod_sub_matrix.index, columns=mod_sub_matrix.index)
df.to_csv('modxmod.csv', index=True, header=True)
df2 = pd.DataFrame(S, index=sub_mod_matrix.index, columns=sub_mod_matrix.index)
df2.to_csv('subxsub.csv', index=True, header=True)

df = pd.read_csv('modxmod.csv', index_col=0)
df2 = pd.read_csv('subxsub.csv', index_col=0)

# convert incidence matrices to adjacency
A = np.matrix(df)
A = np.nan_to_num(A)
AT = np.matrix(df2)
AT = np.nan_to_num(AT)
M = np.dot(A,AT) # 2372 x 2372 mods
S = np.dot(AT,A) # 49 x 49 subs

# create mapping dict to relabel nodes
def get_index_names_dict(df):
    '''takes df where index is list of names
       returns dict of index number:name'''
    d = {}
    for i in range(len(df.index)):
        d[i] = df.index[i]
    return d

M_names = get_index_names_dict(df)
S_names = get_index_names_dict(df2)

'''
np.savetxt('modxmod.csv',M, fmt='%1.0f',delimiter=',')
np.savetxt('subxsub.csv',S)
M = np.genfromtxt('modxmod.csv')
S = np.genfromtxt('subxsub.csv')
'''

# convert np matrices to nx graphs and relabel nodes
M=nx.from_numpy_matrix(M)
S=nx.from_numpy_matrix(S)
nx.relabel_nodes(S,S_names,copy=False)
nx.relabel_nodes(M,M_names,copy=False)

# testing networking algorithms
nx.number_connected_components(M)
sorted(nx.degree(M).values())
nx.clustering(S)
nx.degree(S,'TwoXChromosomes')

# drawing network
nx.draw(S)
nx.draw(S, labels=S_names)

# selecting main components only
x = nx.connected_component_subgraphs(M)
graphs = list(nx.connected_component_subgraphs(M))

giant = max(nx.connected_component_subgraphs(M), key=len)
connected =  M.remove_nodes_from(nx.isolates(M))

# get clustered subs
d = nx.clustering(S)
for k in d.keys():
    if d[k] != 0:
        print k,d[k]
        
# isolates have degree of 2, why?
A = nx.adjacency_matrix(M)
A.setdiag(0)