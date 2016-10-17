# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 12:20:03 2016

@author: msrareg3
"""

def get_node_mode_list(df, nodes):
    '''(df, nodes)
    df with columns 'name' and 'subreddit'
    nodes = list of node names 
    returns list of mode numbers (mod=1,sub=2)
    '''
    n = []
    for node in nodes:
        if node in list(df['name'].unique()):
            n.append(1)
        elif node in list(df['subreddit'].unique()):
            n.append(2)
        else:
            print 'Error: node not found in mod or sub list!'
    return n
