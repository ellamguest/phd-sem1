# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 14:55:02 2016

@author: msrareg3
"""

import networkx as nx
import numpy as np
import pandas as pd

# import weighted adj matrices, convert into graphs
df = pd.read_csv('modxmod.csv', index_col=0)
df2 = pd.read_csv('subxsub.csv', index_col=0)

df = pd.read_csv('default_subs_mods.csv')
df= df[df['Unnamed: 0']==0] # get oldest mod
df = df[['name','subreddit']]
names = list(df['name'].unique()) + list(df['subreddit'].unique())
df['value'] = 1

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

def get_node_mode_dict(nodes):
    d = {}
    for node in nodes:
        if node in list(df['name'].unique()):
            d[node] = 'mod'
        elif node in list(df['subreddit'].unique()):
            d[node] = 'sub'
        else:
            print 'Error: node not found in mod or sub list!'
    return d

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


def get_node_mode_list(nodes):
    n = []
    for node in nodes:
        if node in list(df['name'].unique()):
            n.append(1)
        elif node in list(df['subreddit'].unique()):
            n.append(2)
        else:
            print 'Error: node not found in mod or sub list!'
    return n

n = get_node_mode_list(list(M.nodes()))

nx.draw(M, node_color=n, with_labels=True)

    
