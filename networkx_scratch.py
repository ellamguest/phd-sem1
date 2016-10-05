# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 17:18:28 2016

@author: msrareg3
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pull_sub_info import mod_sub_matrix

df = pd.read_csv('mod_by_sub_matrix.csv')
# df.index = df['name'] - when want to preserve names, now complicates matrices
df = df.drop('name', axis=1)
dfT = df.T
dfT = dfT.reset_index()
dfT = dfT.drop('index', axis=1)

A = np.matrix(df)
AT = np.matrix(dfT)
M = np.dot(A,AT) # 57 x 57 mods
S = np.dot(AT,A) # 24 x 24 subs
np.savetxt('modxmod.csv',M)
np.savetxt('subxsub.csv',S)

M = np.genfromtxt('modxmod.csv')
S = np.genfromtxt('subxsub.csv')

G=nx.from_numpy_matrix(M)
G2=nx.from_numpy_matrix(S)

# look at node attributes
nx.connected_components(G)
sorted(nx.degree(G).values())
nx.clustering(G)
nx.clustering(G2)
nx.degree(G,1)

# drawing network
nx.draw(G2)
plt.savefig("basic_co-moderated_net.png")

# clustering coefficients:
cc = sorted(nx.clustering(G).values())
cc2 = sorted(nx.clustering(G2).values())


plt.plot(cc)
plt.ylabel('clustering coefficient')
plt.show()

# identify nodes by clustering coefficent
 x = nx.clustering(G)
for key,value in x.iteritems():
    if value == 1.0:
        print key

# look at network attributes
nx.node_connectivity(G) # approximation for node connectivity for whole graph
nx.center(G)