# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 12:23:25 2017

@author: msrareg3
"""

import pandas as pd

df = pd.read_csv('td_all_authors.csv')
df['time'] = pd.to_datetime(df['created_utc'], unit='s')
df['1'] = 1
df['author_count'] = df.groupby('author')['1'].transform('count')
df['rank'] = df.groupby('author')['1'].transform('rank')
df['month'] = df.time.dt.to_period('M')
df['month_count'] = df.groupby('month')['1'].transform('count')

counts = df.groupby('author').count()['time']

counts.hist()

grouped = counts.groupby(counts)
g_count = grouped.count()

active = g_count[g_count.index>20]


x = df.head().copy()
x['rank'] = x.groupby('author')['1'].transform('rank')
x['month_count'] = x.groupby([x.time.dt.year, x.time.dt.month])['1'].transform('count')

x['month'] = x.time.dt.to_period('M')


df.groupby(df.date.dt.year).apply(lambda x: x.content.str.contains('feel').sum()/len(x)).plot.barh()

df.groupby(df.date.dt.year).apply(lambda x: x.content.str.contains('feel')/len(x))
