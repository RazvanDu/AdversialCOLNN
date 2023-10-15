import pickle
import datasets
from collections import defaultdict

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

d = defaultdict(lambda: [])

print(f"TODO {len(dataONTO)}")

for i in range(len(dataONTO)):
    print(i)
    print(dataONTO['tokens'][i])
    print(dataONTO['ner_tags_str'][i])
    for j in range(len(dataONTO['tokens'][i])):
        if dataONTO['ner_tags_str'][i][j].startswith("B-"):

            type = dataONTO['ner_tags_str'][i][j].replace("B-", "")

            whole_group = [(dataONTO['ner_tags_str'][i][j], dataONTO['pos_tags'][i][j])]

            while j+1 < len(dataONTO['ner_tags_str'][i]) and dataONTO['ner_tags_str'][i][j+1].startswith("I-"):
                whole_group.append((dataONTO['ner_tags_str'][i][j+1], dataONTO['pos_tags'][i][j+1]))
                j += 1

            print(f"TEST {type} {whole_group}")

            d[type].append(whole_group)



