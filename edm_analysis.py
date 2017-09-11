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


subset = df[['name','id_y','party','title','text','signature_count','proposer','id_x']]
subset.columns = ['name','mp_id','party','title','text','signature_count','proposer','motion_id']
subset.mp_id = subset.mp_id.astype(int)

subset.to_csv('/Users/emg/Desktop/edms/edm-signatures-clean.csv')

'''

#### text analysis
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
import matplotlib.pyplot as plt

def tokenizer(text):
    text = re.sub(r"http\S+", "", text) #remove urls
    text = re.sub('[^A-Za-z0-9]+', ' ', text).strip(' ')
    text = re.findall('[a-zA-Z]{3,}', text)
    tokens = [word.lower() for word in text]
    return tokens

def sentiment(text):
    blob = TextBlob(text)
    pol = blob.sentiment.polarity
    subj = blob.sentiment.subjectivity
    return pol,subj

def sentiment_variables(df):
    df['sentiment'] = df['text'].apply(lambda x: sentiment(x))
    df['polarity'] = df['sentiment'].apply(lambda x: x[0])
    df['subjectivity'] = df['sentiment'].apply(lambda x: x[1])
    return df

def prep_df(df):
    df['tokens'] = df['text'].apply(lambda x: tokenizer(x))
    df['token_length'] = df['tokens'].apply(lambda x: len(x))
    return df


edms = df.drop_duplicates('text')
edms = prep_df(edms)
edms.hist('token_length') # mode around 100 tokens

############## get breakdown of n grams
###### m = document x n gram matrix
###### freq = frew dist of n grams
###### cm = n gram collocation matrix

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['www','http','https','com','','html'])

def ngrams_by_comment(subset, ngram_range=(1, 2), min_df=100):
    corpus = [text for text in subset['text'].dropna() if text is not '∆']
    print('There are {} comments in the corpus'.format(len(corpus)))
    bigram_vectorizer = CountVectorizer(ngram_range = ngram_range, stop_words=stopwords,
                                        lowercase=True,
                                        tokenizer = tokenizer,
                                        min_df = min_df)
    
    B = bigram_vectorizer.fit_transform(corpus)
         
    vocab_dict = bigram_vectorizer.vocabulary_
    inv_map = {v: k for k, v in vocab_dict.items()}
    
    m = pd.DataFrame(B.toarray()).rename(columns=inv_map)
    print('There are {} ngrams in the corpus'.format(m.shape[1]))
    
    freq = m.sum().sort_values(ascending=False)
    cm = m.T.dot(m)
    
    return m, freq, cm

m, freq, cm = ngrams_by_comment(edms, ngram_range=(1,1), min_df=100)

cm.to_csv('/Users/emg/Desktop/edms/semantic-net.csv')



# mp data
mp = pd.read_csv('/Users/emg/Desktop/edms/hocl-ge2015-results-full.csv')




corrections = ['Donaldson, Jeffrey M.',
 'Rogerson, Dan',
 'McCrea, William',
 'Hood, Jimmy',
 'Paisley Jnr, Ian',
 'McDonnell, John Martin',
 'Sharma, Virendra',
 'Hermon, Sylvia',
 'Flello, Rob',
 'Weir, Michael',
 'De Piero, Gloria',
 'Smith, Angela',
 'Slaughter, Andrew',
 'Onwurah, Chi',
 'Farron, Tim',
 'James, Sian',
 'Davies, David',
 'Johnson, Diana',
 'Leslie, Chris',
 'Cash, Bill',
 'Willott, Jennifer',
 'Pound, Steve',
 'de Bois, Nick',
 'Brown, Nick',
 'Bagshawe, Louise',
 'Miliband, Ed',
 'Ashworth, Jon',
 'Iain',
 'Seema',
 'Huhne, Chris',
 'Sawford, Andy',
 'Thornton, Mike',
 'Mike',
 'McDonald, Andrew',
 'Neill, Robert',
 'Liz',
 'Wilson, Robert',
 'Roberts, Liz Saville',
 'Sheikh, Tasmina',
 'Tom, Elliott,',
 'Walker-Lynch, Holly',
 'Olney, Sarah',
 'Vaizey, Edward',
 nan,
 'Little',
 'Joanne',
 'Paul',
 'Gill, Preet',
 'De',
 'Jared'] 
 
 
 ]

missing2 = []
for name in corrections:
    if name not in mps['fullnames'].unique():
        missing2.append(name)
print(len(missing2))

### Iain Duncan Smith, 

x = []
for name in df['mp_id'].unique():
    if name not in mps['Person ID'].unique():
        x.append(name)
print(len(x))

'''
David Evennet 11408 / 17340 - Conservative
Malcolm Rifkind 11660 / 18931 - Conservative
Mensch, Louise 24833 / 9005986
Sawford, Andy 25167 - Labour
Thornton, Mike 25175 - Lib Dem

Tom, Elliott, 9005396 / 13781 - UUP
Olney, Sarah 25596 - Lib Dem
'''




