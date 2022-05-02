
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from collections import defaultdict
import os
import json
def get_pos(text):
    '''
    from pos+offest to pos,offset
    v1809321 -- 'v',1809321
    '''
    try:
        pos=text[0]
        offset=int(text[1:])
        return pos,offset
    except:
        return None
class SentiWordnetCorpusReader():
    """
    Corpus Reader for SentiWordnet
    """
    RESOURCES_FOLDER = 'wordnets'
    SENTIWORDNET_FILE = 'SentiWordNet_3.0.0.json'
    
    def __init__(self, jsonpath=None):
        '''
        import wordnet from json file
        '''
        self.sentiwordnet=defaultdict(set)
        if jsonpath is None:
            file=os.path.join(self.__class__.RESOURCES_FOLDER,self.__class__.SENTIWORDNET_FILE)
        else:
            file=jsonpath
        with open(file,'r') as f:
            data=json.load(f)

        for text,scores in data.items():
            pos,offset=get_pos(text)
            self.sentiwordnet[pos,offset]=scores

    def get_score(self,pos,offset):
        """
        Get sentiment of synset by offset and part of speech
        """
        try:
            return self.sentiwordnet[pos,offset]
        except:
            return None

class MicroWordnetCorpusReader():
    """
    Corpus Reader for SentiWordnet
    """
    RESOURCES_FOLDER = 'wordnets'
    MICROWORDNET_FILE = 'Micro-WNop-WN3.json'
    
    def __init__(self, jsonpath=None):
        '''
        import wordnet from json file
        '''
        self.microwordnet=defaultdict(set)
        if jsonpath is None:
            file=os.path.join(self.__class__.RESOURCES_FOLDER,self.__class__.MICROWORDNET_FILE)
        else:
            file=jsonpath
        with open(file,'r') as f:
            data=json.load(f)

        for text,scores in data.items():
            pos,offset=get_pos(text)
            self.microwordnet[pos,offset]=scores

    def get_score(self, pos,offset):
        """
        Get sentiment of synset by offset and part of speech
        """
        try:
            return self.microwordnet[pos,offset]
        except:
            return None




def sentiwordnet_sentiment(self):
    """
    Expand Wordnet with sentiwordnet
    """
    if not hasattr(self.__class__, 'sentiwordnet_reader'):
        self.__class__.sentiwordnet_reader = SentiWordnetCorpusReader()
    return self.__class__.sentiwordnet_reader.get_score(self.pos(),self.offset() )

def microwordnet_sentiment(self):
    """
    Expand Wordnet with microwordnet
    """
    if not hasattr(self.__class__, 'microwordnet_reader'):
        self.__class__.microwordnet_reader = MicroWordnetCorpusReader()

    return self.__class__.microwordnet_reader.get_score(self.pos(),self.offset() )

#Expand
Synset.senti = sentiwordnet_sentiment
Synset.micro_senti = microwordnet_sentiment

if __name__ == "__main__":
    good = wn.synset('good.a.13')
    print(f'sentiment score of {good.name()}: {good.senti()}')
    print(f'micro sentiment score of {good.name()}: {good.micro_senti()}')

    