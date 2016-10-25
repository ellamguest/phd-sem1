# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:51:58 2016

@author: emg
"""

import pandas as pd

df = pd.read_csv('/Users/emg/Programmming/GitHub/phd-sem1/default_subs.csv', index_col=0)

text = df[['display_name','submit_text', 'public_description']]

text.to_csv('defs_text.csv')