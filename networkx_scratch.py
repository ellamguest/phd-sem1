# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 17:18:28 2016

@author: msrareg3
"""

import networkx as nx
import numpy as np
import pandas as pd
from pull_sub_info import mod_sub_matrix

df = pd.read_csv('mod_by_sub_matrix.csv')
# df.index = df['name'] - when want to preserve names, now complicates matrices
df = df.drop('name', axis=1)
dfT = df.T
dfT = dfT.reset_index()
dfT = dfT.drop('index', axis=1)

A = np.matrix(df)
AT = np.matrix(dfT)
M = np.dot(A,AT) # 57 x 57

G=nx.from_numpy_matrix(M)

# look at metwrok attributes
nx.connected_components(G)
sorted(nx.degree(G).values())
nx.clustering(G)