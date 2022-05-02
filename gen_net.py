import  xml.dom.minidom
import os
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
import json
'''
generate json document for sentiwordnets

format
{pos+offset:senti scores}

e.x.: for Synset('overwhelm.v.01')

"v1809321": [0.38,0.38,0.0,1.0]
'''
SWNS_PATH='sentiwordnets'
# VN_PATH='new_vn'
# VN_FILES=os.listdir(VN_PATH)
SWNS_FILES=os.listdir(SWNS_PATH)
OUTPUT_PATH='wordnets'

def get_synset(pos,offset):
    try:
        synset=wn.synset_from_pos_and_offset(pos,offset)
        return synset.pos(),synset.offset()
    except:
        return pos,offset


#Micro-WNop-WN3.txt
outfile=os.path.join(OUTPUT_PATH,'Micro-WNop-WN3.json')
file=os.path.join(SWNS_PATH,'Micro-WNop-WN3.txt')
micro_v3=dict()
with open(file, 'rb') as f:
    line=f.readline()
    while line:
        if line.startswith(b'# begin Group1'):
            break
        if line.startswith(b'#') or line.startswith(b' '):#35-'#' in bytes
            line=f.readline()
            continue
        sets = line.split(b'\t')
        try:
            synset= sets[2]
            scores=sets[0:2]
            scores=[float(x) for x in scores]
            pos=str(synset.decode("utf-8")[0])
            offset=int(synset.decode("utf-8")[1:])
            pos,offset=get_synset(pos,offset)
            micro_v3[str(pos)+str(offset)] = scores
            line=f.readline()
        except ValueError:
            line=f.readline()
            continue
    while line:
        if line.startswith(b'# begin Group2'):
            break
        if line.startswith(b'#') or line.startswith(b' '):#35-'#' in bytes
            line=f.readline()
            continue
        sets = line.split(b'\t')
        try:
            synset= sets[6]
            scores=sets[0:6]
            scores=[float(x) for x in scores]
            pos=str(synset.decode("utf-8")[0])
            offset=int(synset.decode("utf-8")[1:])
            pos,offset=get_synset(pos,offset)
            micro_v3[str(pos)+str(offset)] = scores
            line=f.readline()
        except ValueError:
            line=f.readline()
            continue
    while line:
        if line.startswith(b'#') or line.startswith(b' '):#35-'#' in bytes
            line=f.readline()
            continue
        sets = line.split(b'\t')
        try:
            synset= sets[4]
            scores=sets[0:4]
            scores=[float(x) for x in scores]
            pos=str(synset.decode("utf-8")[0])
            offset=int(synset.decode("utf-8")[1:])
            pos,offset=get_synset(pos,offset)
            micro_v3[str(pos)+str(offset)] = scores
            line=f.readline()
        except ValueError:
            line=f.readline()
            continue
with open(outfile, "w") as f:
    json.dump(micro_v3, f, indent=4)



#SentiWordNet_3.0.0.txt
outfile=os.path.join(OUTPUT_PATH,'SentiWordNet_3.0.0.json')
file=os.path.join(SWNS_PATH,'SentiWordNet_3.0.0.txt')
swn_v3=dict()
with open(file, 'rb') as f:
    line=f.readline()
    while line:
        if line.startswith(b'#') or line.startswith(b' '):#35-'#' in bytes
            line=f.readline()
            continue
        sets = line.split(b'\t')
        try:
            pos, offset= sets[0:2]
            scores=sets[2:4]
            scores=[float(x) for x in scores]
            swn_v3[str(pos.decode("utf-8"))+str(int(offset))] = scores
            pos=str(pos.decode("utf-8"))
            offset=int(offset.decode("utf-8"))
            pos,offset=get_synset(pos,offset)
            swn_v3[str(pos)+str(offset)] = scores
            line=f.readline()
        except ValueError:
            line=f.readline()
            continue
with open(outfile, "w") as f:
    json.dump(swn_v3, f, indent=4)


    