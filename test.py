
from nltk.corpus import wordnet as wn
import sentiwordnet

if __name__ == "__main__":
    good = wn.synset('good.a.13')
    print(f'sentiment score of {good.name()}: {good.senti()}')
    print(f'micro sentiment score of {good.name()}: {good.micro_senti()}')

    