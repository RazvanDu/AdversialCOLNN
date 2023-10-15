import pickle
import datasets
from collections import defaultdict
from numba import jit, cuda

from multiprocessing import Pool

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

print(f"TODO {len(dataONTO)}")

def process(tokens, ner_tags, pos_tags, d):
    for j in range(len(tokens)):
        if ner_tags[j][0] == 'B' and ner_tags[j][1] == '-':

            type = ner_tags[j].replace("B-", "")

            whole_group = [(tokens[j], pos_tags[j])]

            while j+1 < len(tokens) and ner_tags[j+1].startswith("I-"):
                whole_group.append((tokens[j+1], pos_tags[j+1]))
                j += 1

            d[type].append(whole_group)

def process_2(i):

    d = {"O": [], "PERSON": [], "NORP": [], "FAC": [], "ORG": [], "GPE": [], "LOC": [], "PRODUCT": [], "DATE": [],
         "TIME": [], "PERCENT": [], "MONEY": [], "QUANTITY": [], "ORDINAL": [], "CARDINAL": [], "EVENT": [],
         "WORK_OF_ART": [], "LAW": [], "LANGUAGE": []}

    print(i)
    process(dataONTO['tokens'][i], dataONTO['ner_tags_str'][i], dataONTO['pos_tags'][i], d)

    return d

with Pool(256) as p:
    numbers = p.map(process_2, range(dataONTO))

d = {"O": set(), "PERSON": set(), "NORP": set(), "FAC": set(), "ORG": set(), "GPE": set(), "LOC": set(), "PRODUCT": set(), "DATE": set(), "TIME": set(), "PERCENT": set(), "MONEY": set(), "QUANTITY": set(), "ORDINAL": set(), "CARDINAL": set(), "EVENT": set(), "WORK_OF_ART": set(), "LAW": set(), "LANGUAGE": set()}

for dict in numbers:
    for val in dict.keys():
        for actual_val in dict[val]:
            d[val].add(tuple(actual_val))

print(numbers)


with open('dictionary.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(d, file)

with open('dictionary.pkl', 'rb') as f:
    d = pickle.load(f)

print("D ", d)

