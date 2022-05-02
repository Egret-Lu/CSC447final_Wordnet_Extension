
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from collections import defaultdict
from xml.dom.minidom import  parse
import os
import json
# def get_pos(text):
#     '''
#     from pos+offest to pos,offset
#     v1809321 -- 'v',1809321
#     '''
#     try:
#         pos=text[0]
#         offset=int(text[1:])
#         return pos,offset
#     except:
#         return None
class VerbnetClass():
    VN_PATH='new_vn'
    def __init__(self,class_text='accept-77'):
        file=class_text+'.xml'
        xmlfile=os.path.join(self.__class__.VN_PATH,file)
        try:
            dom = parse(xmlfile)
            data=dom.documentElement
            members = data.getElementsByTagName('MEMBERS')[0].getElementsByTagName('MEMBER')
            roles=data.getElementsByTagName('THEMROLES')[0].getElementsByTagName('THEMROLE')
            frames=data.getElementsByTagName('FRAMES')[0].getElementsByTagName('FRAME')
            self.__roles=[]
            self.__frames=[]
            for role in roles:
                self.__roles.append(role.getAttribute('type'))
            for frame in frames:
                self.__frames.append(frame.getElementsByTagName('DESCRIPTION')[0].getAttribute('primary'))
        except:
            raise ValueError('Invalid Verbnet Class')
    def get_roles(self):
        return self.__roles
    def get_frames(self):
        return self.__frames







class VerbnetCorpusReader():
    """
    Corpus Reader for Verbnet
    """
    RESOURCES_FOLDER = 'wordnets'
    SENTIWORDNET_FILE = 'Verbnet.json'
    VN_PATH='new_vn'
    
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

        for text,xmlfiles in data.items():
            self.sentiwordnet[text]=xmlfiles

    def get_classes(self,text):
        """
        Get class list of verb 
        each verb may accord with multiple classes
        """
        try:
            xmlfiles=self.sentiwordnet[text]
            classes=[VerbnetClass(xmlfile.replace('.xml','')) for xmlfile in xmlfiles]
            return classes
        except:
            return []

    # def get_roles(self,text):
    #     """
    #     Get sentiment of synset by offset and part of speech
    #     """
    #     try:
    #         xmlfile=os.path.join(self.__class__.VN_PATH,self.sentiwordnet[text][0])
    #         dom = parse(xmlfile)
    #         data=dom.documentElement
    #         roles=data.getElementsByTagName('THEMROLES')[0].getElementsByTagName('THEMROLE')
    #         themroles=[]
    #         for role in roles:
    #             themroles.append(role.getAttribute('type'))
    
    #         return themroles
    #     except:
    #         return []







def verbnet_classes(self):
    """
    Expand Wordnet with microwordnet
    """
    if not hasattr(self.__class__, 'verbnet_reader'):
        self.__class__.verbnet_reader = VerbnetCorpusReader()
    return self.__class__.verbnet_reader.get_classes(self.name() )

#Expand
Synset.vn_classes = verbnet_classes


if __name__ == "__main__":
    encourage = wn.synset('encourage.v.02')
    print('get verbnet class list for encourage.v.02')
    print(encourage.vn_classes())
    print('get frame list for the first class of encourage.v.02')
    print(encourage.vn_classes()[0].get_frames())

    