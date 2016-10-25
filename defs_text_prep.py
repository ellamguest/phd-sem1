# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:51:58 2016

@author: emg
"""

import pandas as pd
import string
from textblob import TextBlob, Word
import random
import sys

df = pd.read_csv('/Users/emg/Programmming/GitHub/phd-sem1/default_subs.csv', index_col=0)
text = df[['display_name','submit_text', 'public_description']]
text['public_description'] = text['public_description'].fillna('')
text['submit_text'] = text['submit_text'].fillna('')


# own word parsing
def get_words(text):
    words = []
    text = text.lower()
    for x in text.split():
        words.append(x.strip(string.punctuation))
    return words

text['desc_words'] = text['public_description'].apply(get_words)
text['submit_words'] = text['submit_text'].apply(get_words)

text.to_csv('defs_text.csv')
text.to_csv('defs_text.txt')
text = pd.read_csv('defs_text.csv')

# text analysis w/ textblob

x = text.iloc[0]['public_description']
blob = TextBlob(x)
blob.tags #returns POS tags
blob.noun_phrases # extracts noun phrases
blob.sentiment.polarity # postive or negative sentiment leaning
blob.sentences # can analyse sentences separately
blob.words # or words
blob.correct() # correct any spelling mistakes
word.spellcheck() # return correct word and confidence rating

# analysing def descriptions
df = pd.read_csv('default_abouts.csv', index_col=0)

def get_polarity(text):
    text = text.decode('ascii', errors="replace")
    b = TextBlob(text)
    return b.sentiment.polarity

df['polarity'] = df['description'].apply(get_polarity)