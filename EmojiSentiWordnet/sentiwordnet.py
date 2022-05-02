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

class synset():
    def __init__(self,pos_score=None,neg_score=None,uid=None,occ_rate=None,des=None):
        '''
        build a sysnet object for each emoji character
        '''
        self.__ps=pos_score #positive score
        self.__ns=neg_score #negative score
        self.__occ=occ_rate #occurance rate
        self.__uid=uid #id in unicode
        self.__des=des #description
    def get_pscore(self):
        return self.__ps
    def get_nscore(self):
        return self.__ns
    def get_occ(self):
        return self.__occ
    def get_des(self):
        return self.__des
    def get_id(self):
        return self.__uid


class mojiSentiWordnet():
    """
    Construct a new SentiWordNet  Reader, using data from
    the emoji file.
    """
    def __init__(self, jsonfile='emoji_senti.json', encoding="utf-8"):
        with open(jsonfile,'r') as f:
            emoji_senti=json.load(f)
        self.dict={}
        emoji_icons=emoji_senti['id'].keys()
        for emoji_icon in emoji_icons:
            emoji_synset=synset(emoji_senti['pos_score'][emoji_icon],emoji_senti['neg_score'][emoji_icon],emoji_senti['id'][emoji_icon],emoji_senti['occ_rate'][emoji_icon],emoji_senti['des'][emoji_icon])
            self.dict[emoji_icon]=emoji_synset
    def synset(self,lemma=None):
        if lemma in self.dict.keys():
            return self.dict[lemma]
        else:
            return None

def main():
    mojiSentiWordnet()
    print('Set for emoji senti wordnet V0.0')
    return mojiSentiWordnet()

if __name__ == '__main__':
    main()

