# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 14:04:09 2016

@author: emg
"""
from network_functions import get_node_mode_list

def get_index_names_dict(df):
    '''takes df where index is list of names
       returns dict of index number:name'''
    d = {}
    for i in range(len(df.index)):
        d[i] = df.index[i]
    return d


df = pd.read_csv('default_subs_mods.csv')
orgs = list(df[df['Unnamed: 0']==0]['name'].unique())
df['value'] = 1
m = df.pivot('name','subreddit','value').fillna(0)
x = m.loc[m.index.isin(orgs)]

aff = np.matrix(x)
M = np.dot(aff.transpose(), aff)
np.fill_diagonal(M, 0)

G=nx.from_numpy_matrix(M)
M_names = get_index_names_dict(x.transpose())
nx.relabel_nodes(G,M_names,copy=False)
G.remove_nodes_from(nx.isolates(G))


nx.draw(G, with_labels=True)