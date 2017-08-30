# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 11:57:29 2017

@author: msrareg3
"""

years = ['2013','2014','2015','2016','2017']
months = ["%.2d" % i for i in range(1, 13)]

dates = []
for year in years:
    for month in months:
        dates.append(year + '_' + month)
        
td_dates = dates[5:-5]

datasets = []
for date in td_dates:
    datasets.append('[fh-bigquery:reddit_comments.{}]'.format(date))

s = ''
for d in datasets:
    s += d + ', '