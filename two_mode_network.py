# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 14:55:02 2016

@author: msrareg3
"""

import numpy as np
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
from network_functions import get_node_mode_list

# import weighted adj matrices, convert into graphs
df = pd.read_csv('modxmod.csv', index_col=0)
df2 = pd.read_csv('subxsub.csv', index_col=0)

df = pd.read_csv('default_subs_mods.csv')
df= df[df['Unnamed: 0']==0] # get oldest mod
df = df[['name','subreddit']]
df['value'] = 1

names = list(df['name'].unique()) + list(df['subreddit'].unique())

A = pd.DataFrame(index=list(df['name'].unique()), columns=df['name'].unique())
B = df.pivot('name', 'subreddit', 'value')
C = df.pivot('subreddit', 'name','value')
D = pd.DataFrame(index=list(df['subreddit'].unique()), columns=df['subreddit'].unique())

AB = pd.concat([A,B], axis=1)
CD = pd.concat([C,D], axis=1)
m = pd.concat([AB,CD]).fillna(0)

''''
A | B
- - -
C | D

A = mod x mod (45 x 45)
B = mod x sub (45 x 49)
C = sub x mod (49 x 45)
D = sub x sub (49 x 49)

m = (mod + sub) x (mod + sub)  (94 x 94)
'''

# m.to_csv('default_subs_mods_2mode.csv')


d = get_node_mode_dict(list(m.index))

M = nx.Graph(np.matrix(m))

def get_index_names_dict(df):
    '''takes df where index is list of names
       returns dict of index number:name'''
    d = {}
    for i in range(len(df.index)):
        d[i] = df.index[i]
    return d

M_names = get_index_names_dict(m)
nx.relabel_nodes(M,M_names,copy=False)
nx.set_node_attributes(M, 'mode', d)



n = get_node_mode_list(list(M.nodes()))

nx.draw(M, node_color=n, with_labels=True)

# attempting to import as edgelist
df = pd.read_csv('default_subs_mods.csv')
df['value'] = 1

B = nx.Graph()
B.add_nodes_from(list(df['name'].unique()), bipartite=0)
B.add_nodes_from(list(df['subreddit'].unique()), bipartite=1)
B.add_weighted_edges_from(zip(list(df['name']),list(df['subreddit']),list(df['value'])))

#mod_nodes, sub_nodes = bipartite.sets(B)

#==============================================================================
# n = get_node_mode_list(df,list(B.nodes()))
# nx.draw(B, with_labels=True, node_color=n)
#==============================================================================


# only look at nodes with degree > 1
con = []
for key, value in B.degree().iteritems():
     if value >2:
         con.append(key)

C = B.subgraph(con)
n = get_node_mode_list(df,list(C.nodes()))
nx.draw(C, with_labels=True, node_color=n)

