#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 13:31:01 2017

@author: emg
"""

import pandas as pd
import numpy as np

df = pd.read_csv('/Users/emg/Desktop/edms/edm-signatures-2010-2017.csv', index_col=0)
df.replace('Tom, Elliott,', 'Elliott, Tom', inplace=True)
df.replace('Iain', 'McKenzie, Iain', inplace=True)
df.replace(17340, 11408, inplace=True) # David Evennett id wrong
df.replace(9005396, 13781, inplace=True) # Tom Elliott id wrong
df.replace(9005986, 24833, inplace=True) # Louise Mensch id wrong
df.replace('Bagshawe, Louise', 'Mensch, Louise', inplace=True) # Louise Mensch id wrong
df.replace(9006242, 25452, inplace=True) # Emma Little Pengelly id wrong
df['mp_sign_count'] = df.groupby('mp_id')['id'].transform('count')

df.ix[df['mp_id']>9000000, 'mp'] = np.nan
df.dropna(how='any', inplace=True)

mps17 = pd.read_csv('/Users/emg/Desktop/edms/mps.csv')
mps15 = pd.read_csv('/Users/emg/Desktop/edms/mps_2015.csv')
mps10 = pd.read_csv('/Users/emg/Desktop/edms/mps_2010.csv')
mps05 = pd.read_csv('/Users/emg/Desktop/edms/mps_2005.csv')
mps = pd.concat([mps17, mps15, mps10, mps05])
mps['fullname'] = mps['Last name'] +', ' + mps['First name']

### cross-checking ids & names
names = df.drop_duplicates('mp')[['mp','mp_id']]

mps_dict = dict(zip(mps['Person ID'], mps['fullname']))
names['name'] = names['mp_id'].map(lambda x: mps_dict[x] if x in mps_dict.keys() else None).fillna(names['mp'])

d = dict(zip(mps['fullname'], mps['Person ID']))
names['id'] = names['name'].map(lambda x: d[x] if x in d.keys() else None).fillna(names['mp_id'])

mp_party_dict = dict(zip(mps['fullname'], mps['Party']))
names['party'] = names['name'].map(lambda x: mp_party_dict[x] if x in mp_party_dict.keys() else None)


# mps not in the twfu datasets because they were in power betweens general elections
skipped_mps = {'Sawford, Andy': 'Labour',
'Thornton, Mike': 'Liberal Democrat',
'Olney, Sarah':'Liberal Democrat',
'McKenzie, Iain':'Labour'}

for k,v in skipped_mps.items():
    names.ix[names['mp']==k, 'party']=v

df = pd.merge(df, names, on='mp', how='inner')

s = df.groupby('name').count()['mp']
p = df.drop_duplicates('title').groupby('proposer').count()['mp']
c = pd.DataFrame({'scount':s,'pcount':p}).fillna(0)
c['party'] = c.index.map(lambda x: mp_party_dict[x] if x in mp_party_dict.keys() else None)
c['name'] = c.index
 
party_cols = {'Labour':'red',
         'Conservative':'blue',
        'Scottish National Party':'yellow',
       'Labour/Co-operative':'pink',
       'Liberal Democrat':'orange',
       None:'black',
       'DUP':'grey',
       'Sinn Féin':'grey',
       'Social Democratic and Labour Party':'grey', 
       'Plaid Cymru':'grey',
       'UUP':'grey',
       'Respect':'grey',
       'Alliance':'grey',
       'Green':'green'}
c['colour']=c['party'].map(lambda x:party_cols[x]) 

test = c.head(20)
data = [list(x) for x in list(zip(test.scount,test.pcount,test.name,test.colour, test.party))]
data

pd.DataFrame(data).to_csv('/Users/emg/Google Drive/PhD/data journalism/project-folder/counts_sample.csv', header=False, index=False)

c[['pcount','scount']].to_csv('/Users/emg/Google Drive/PhD/data journalism/project-folder/tuples.csv', header=False, index=False)

subset = df[['name','id_y','party','title','text','signature_count','proposer','id_x']]
subset.columns = ['name','mp_id','party','title','text','signature_count','proposer','motion_id']
subset.mp_id = subset.mp_id.astype(int)

subset.to_csv('/Users/emg/Desktop/edms/edm-signatures-clean.csv')

subset = pd.read_csv('/Users/emg/Desktop/edms/edm-signatures-clean.csv', index_col=0)
df = subset
s = df.groupby('name').count()['party']
p = df.drop_duplicates('title').groupby('proposer').count()['party']
c = pd.DataFrame({'scount':s,'pcount':p}).fillna(0)

