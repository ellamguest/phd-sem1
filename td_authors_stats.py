# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 12:23:25 2017

@author: msrareg3
"""

import pandas as pd

df = pd.read_csv('td_all_authors.csv')
df['time'] = pd.to_datetime(df['created_utc'], unit='s')

counts = df.groupby('author').count()['time']

counts.hist()

grouped = counts.groupby(counts)
g_count = grouped.count()

active = g_count[g_count.index>20]