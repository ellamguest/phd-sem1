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

nx.draw(M)
nx.draw(M, labels=M_names)

S.remove_nodes_from(nx.isolates(S))
nx.draw(S)
nx.draw(S, labels=S_names)