# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:53:08 2016

@author: emg
"""

import pandas as pd

df = pd.read_csv('default_subs_mods.csv')
mods = list(df['name'])

#NOT CURRENTLY POSSIBLE VIA API, WOULD NEED TO SCRAPE