import pickle 
from nltk.corpus import wordnet as wn
from nltk.corpus import verbnet as vb
import nltk
from pprint import pprint
from operator import itemgetter
from nltk.corpus import framenet as fn
from nltk.corpus.reader.framenet import PrettyList
from nltk.corpus import sentiwordnet as swn
import emoji
import os
import codecs
import pandas as pd
import advertools as adv
from bs4 import BeautifulSoup
import requests
import json

#Data set with sentimental analysis on tweet
emoji_all=emoji.UNICODE_EMOJI['en'].keys()
emoji_dict=emoji.UNICODE_EMOJI['en']
f = open('emoji_tweets_preprocessed_withEMOJI.pkl', 'rb')   # Pickle file is newly created where foo1.py is
tweet_pre=pickle.load(f)
tweets=tweet_pre['tweets']
labels=tweet_pre['labels']

#extract all emoji
emojis=[]
other=[]
tweet_pre['emoji_icon']=[]
for tweet in tweets:
    tweet_emoji=adv.extract_emoji(tweet)['emoji_flat']
#         line=[c for c in line if c in emoji_all]
    tweet_pre['emoji_icon'].append(list(set(tweet_emoji)))
    for emoji_icon in tweet_emoji:
        if emoji_icon not in emojis:
            if emoji_icon in emoji_all:
                emojis.append(emoji_icon)
            elif emoji_icon not in other:
                other.append(emoji_icon)
    line=f.readline()


assert len(tweet_pre['tweets'])==len(tweet_pre['labels'])&len(tweet_pre['labels'])==len(tweet_pre['emoji_icon'])


#build data set for all emoji
emoji_df=pd.DataFrame(tweet_pre)
emoji_df=emoji_df.explode("emoji_icon")
emoji_senti=emoji_df.groupby("emoji_icon").agg(['count','sum'])['labels']
emoji_senti.columns=['sum','pos']
emoji_senti['neg']=emoji_senti['sum']-emoji_senti['pos']
emoji_senti['pos_score']=emoji_senti['pos']/emoji_senti['sum']
emoji_senti['neg_score']=emoji_senti['neg']/emoji_senti['sum']
emoji_senti=emoji_senti.sort_values(by=['sum'], ascending=False)
emoji_senti=emoji_senti.reset_index()
emoji_senti['id']=emoji_senti['emoji_icon'].apply(lambda x: '{:X}'.format(ord(x)))
emoji_senti=emoji_senti[emoji_senti['sum']>=10]


#craw data from emoji use on Twitter in real-time http://emojitracker.com/
with open('emoji_use.html','rb') as f:
    soup = BeautifulSoup(f, 'html.parser')

emoji_links=soup.find_all('section')[0].find_all('li')
emoji_cnt=dict()
for link in emoji_links:
    emoji_cnt[link.get('id')]=int(link.get_text().strip())

emoji_senti['cnt']=emoji_senti['id'].apply(lambda x: emoji_cnt[x])
emoji_senti['occ_rate']=emoji_senti['cnt']/(emoji_senti['cnt'].sum())
emoji_senti['des']=emoji_senti['emoji_icon'].apply(lambda x: emoji_dict[x])
emoji_senti.set_index('emoji_icon').to_json('EmojiSentiWordnet/emoji_senti.json',orient='columns',indent=2)
# emoji_json=None
# emoji_senti.set_index('emoji_icon').to_json(emoji_json,orient='columns')

# with open('emoji_senti.json', 'w') as f:
#   json.dump(emoji_json, f, indent=2)
