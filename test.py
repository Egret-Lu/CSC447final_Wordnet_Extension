
from nltk.corpus import wordnet as wn
import sentiwordnet
import verbnet
    


if __name__ == "__main__":
    good = wn.synset('good.a.13')
    print(f'sentiment score of {good.name()}: {good.senti()}')
    print(f'micro sentiment score of {good.name()}: {good.micro_senti()}')
    encourage = wn.synset('encourage.v.02')
    #get verbnet class list for encourage.v.02
    print(encourage.vn_classes())
    #get frame list for the first class of encourage.v.02 which is accept-77
    print(encourage.vn_classes()[0].get_frames())
    print(encourage.vn_classes()[0].get_roles())

    