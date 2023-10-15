import pickle
import datasets
from collections import defaultdict
from numba import jit, cuda

dataCONLL = ""
dataONTO = ""

with open('conll.pkl', 'rb') as f:
    dataCONLL = pickle.load(f)

with open('OntoNotes.pkl', 'rb') as f:
    dataONTO = pickle.load(f)

print(dataCONLL['tokens'][100])
print(dataCONLL['ner_tags_str'][100])
print(dataCONLL['pos_tags'][100])
print(dataCONLL['doc'][100])
print(dataONTO)

d = {"O": [], "PERSON": [], "NORP": [], "FAC": [], "ORG": [], "GPE": [], "LOC": [], "PRODUCT": [], "DATE": [], "TIME": [], "PERCENT": [], "MONEY": [], "QUANTITY": [], "ORDINAL": [], "CARDINAL": [], "EVENT": [], "WORK_OF_ART": [], "LAW": [], "LANGUAGE": []}

print(f"TODO {len(dataONTO)}")

def process(tokens, ner_tags, pos_tags):
    for j in range(len(tokens)):
        if ner_tags[j].startswith("B-"):

            type = ner_tags[j].replace("B-", "")

            whole_group = [(ner_tags[j], pos_tags[j])]

            while j+1 < len(ner_tags) and ner_tags[j+1].startswith("I-"):
                whole_group.append((ner_tags[j+1], pos_tags[j+1]))
                j += 1

            print(f"TEST {type} {whole_group}")

            d[type].append(whole_group)

for i in range(len(dataONTO)):
    print(i)
    process(dataONTO['tokens'][i], dataONTO['ner_tags_str'][i], dataONTO['pos_tags'][i])

    # Open a file and use dump()

    if i%10 == 0:

        with open('dictionary.pkl', 'wb') as file:
            # A new file will be created
            pickle.dump(d, file)

with open('dictionary.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(d, file)


