# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 17:18:28 2016

@author: msrareg3
"""

import networkx as nx
import numpy as np
from pull_sub_info import mod_sub_matrix

A= np.matrix(mod_sub_matrix) # need to convert incidence matrix to adjacency
G=nx.from_numpy_matrix(A)